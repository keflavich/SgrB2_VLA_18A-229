def fix_intents(vis,
                bad_intent='CALIBRATE_BANDPASS#UNSPECIFIED,CALIBRATE_FLUX#UNSPECIFIED',
                replacement_intent='CALIBRATE_FLUX#UNSPECIFIED'):
    """
    With lots of inspiration from Todd Hunter's editIntents
    """

    tb.open(vis+"/STATE", nomodify=False)

    obs_mode = tb.getcol("OBS_MODE")

    match = obs_mode == bad_intent
    if not match.any():
        raise ValueError("No matches to intent {0} found.".format(bad_intent))

    obs_mode[match] = replacement_intent

    tb.putcol('OBS_MODE', obs_mode)
    tb.close()
