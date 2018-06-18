from taskinit import casac, tbtool
import numpy as np

tb = tbtool()

def id_spw(vis, freq, min_chan=255):
    tb.open(vis+"/SPECTRAL_WINDOW")
    nchans = tb.getcol('NUM_CHAN')
    for spwnum, nchan in enumerate(nchans):
        if nchan < min_chan:
            continue
        else:
            frqs = tb.getcol("CHAN_FREQ", startrow=spwnum, nrow=1)
            minfrq, maxfrq = frqs.min(), frqs.max()
            if (minfrq < freq) and (maxfrq > freq):
                return spwnum

    raise ValueError("No match for frequency {0} found in {1}"
                     .format(freq, vis))

def id_spws(vislist, freq):
    return ",".join([str(id_spw(ms, freq)) for ms in vislist])


def get_spw_mapping(vis, caltable):
    """
    Obtain a spwmap mapping a calibration table to a specific observation using
    the metadata in the measurement set and the caltable.  The returned spwmap
    should be passable to `applycal`.
    """

    tb.open(caltable+"/SPECTRAL_WINDOW")
    cal_freqs = tb.getcol('CHAN_FREQ')[0,:]
    tb.close()

    tb.open(caltable+"/OBSERVATION")
    caltimes = tb.getcol('TIME_RANGE')
    calstarttimes,calendtimes = caltimes
    calmidtimes = caltimes.mean(axis=0)
    tb.close()

    tb.open(caltable)
    obsids = tb.getcol('OBSERVATION_ID')
    spw_ids = tb.getcol('SPECTRAL_WINDOW_ID')
    tb.close()


    tb.open(vis+"/OBSERVATION")
    obs_time = tb.getcol('TIME_RANGE')
    tb.close()

    closest_cal = np.argmin(np.abs(obs_time.mean()-calmidtimes)) 
    assert obs_time[0] < calmidtimes[closest_cal] < obs_time[1]

    obs_match = obsids == closest_cal
    spws_match = np.unique(spw_ids[obs_match])

    obs_cal_freqs = cal_freqs[spws_match]

    spwmap = []

    tb.open(vis+"/SPECTRAL_WINDOW")
    nchans = tb.getcol('NUM_CHAN')
    tb.close()
    for spwnum, nchan in enumerate(nchans):
        tb.open(vis+"/SPECTRAL_WINDOW")
        frqs = tb.getcol("CHAN_FREQ", startrow=spwnum, nrow=1)
        tb.close()

        meanfreq = frqs.mean()
        closest_freq = np.argmin(np.abs(meanfreq-obs_cal_freqs))
        
        spwmap.append(closest_freq)

    return spwmap
