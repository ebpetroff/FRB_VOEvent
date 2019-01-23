

def NewVOEvent(dm, dm_err, width, snr, flux, ra, dec, semiMaj, semiMin, ne2001, name, importance, utc, gl, gb): 

    z = dm/1200.0  #May change
    errDeg = semiMaj/60.0

    # Parse UTC
    utc_YY = int(utc[:4])
    utc_MM = int(utc[5:7])
    utc_DD = int(utc[8:10])
    utc_hh = int(utc[11:13])
    utc_mm = int(utc[14:16])
    utc_ss = float(utc[17:])
    t = Time('T'.join([utc[:10], utc[11:]]), scale='utc', format='isot')
    mjd = t.mjd
    
    now = Time.now()
    mjd_now = now.mjd
   
    ivorn = ''.join([name, str(utc_hh), str(utc_mm), '/', str(mjd_now)]) 

    v = vp.Voevent(stream='nl.astron.apertif/alert', stream_id=ivorn, role=vp.definitions.roles.observation)
    # Author origin information
    vp.set_who(v, date=datetime.datetime.utcnow(), author_ivorn="nl.astron")
    # Author contact information
    vp.set_author(v, title="ASTRON ALERT FRB Detector", contactName="Leon Oostrum", contactEmail="leonoostrum@gmail.com", shortName="ALERT")
    # Parameter definitions

    #Apertif-specific observing configuration %%TODO: update parameters as necessary for new obs config
    beam_sMa = vp.Param(name="beam_semi-major_axis", unit="MM", ucd="instr.beam;pos.errorEllipse;phys.angSize.smajAxis", ac=True, value=semiMaj)
    beam_sma = vp.Param(name="beam_semi-minor_axis", unit="MM", ucd="instr.beam;pos.errorEllipse;phys.angSize.sminAxis", ac=True, value=semiMin)
    beam_rot = vp.Param(name="beam_rotation_angle", value=0.0, unit="Degrees", ucd="instr.beam;pos.errorEllipse;instr.offset", ac=True)
    tsamp = vp.Param(name="sampling_time", value=0.0496, unit="ms", ucd="time.resolution", ac=True)
    bw = vp.Param(name="bandwidth", value=300.0, unit="MHz", ucd="instr.bandwidth", ac=True)
    nchan = vp.Param(name="nchan", value="1536", dataType="int", ucd="meta.number;em.freq;em.bin", unit="None")
    cf = vp.Param(name="centre_frequency", value=1400.0, unit="MHz", ucd="em.freq;instr", ac=True)
    npol = vp.Param(name="npol", value="2", dataType="int", unit="None")
    bits = vp.Param(name="bits_per_sample", value="8", dataType="int", unit="None")
    gain = vp.Param(name="gain", value=1.0, unit="K/Jy", ac=True)
    tsys = vp.Param(name="tsys", value=75.0, unit="K", ucd="phot.antennaTemp", ac=True)
    backend = vp.Param(name="backend", value="ARTS")
#    beam = vp.Param(name="beam", value= )

    v.What.append(vp.Group(params=[beam_sMa, beam_sma, beam_rot, tsamp, bw, nchan, cf, npol, bits, gain, tsys, backend], name="observatory parameters"))

    #Event parameters
    DM = vp.Param(name="dm", ucd="phys.dispMeasure", unit="pc/cm^3", ac=True, value=dm )
    DM_err = vp.Param(name="dm_err", ucd="stat.error;phys.dispMeasure", unit="pc/cm^3", ac=True, value=dm_err)
    Width = vp.Param(name="width", ucd="time.duration;src.var.pulse", unit="ms", ac=True, value=width)
    SNR = vp.Param(name="snr", ucd="stat.snr", unit="None", ac=True, value=snr)
    Flux = vp.Param(name="flux", ucd="phot.flux", unit="Jy", ac=True, value=flux)
    Flux.Description = "Calculated from radiometer equation. Not calibrated."
    Gl = vp.Param(name="gl", ucd="pos.galactic.lon", unit="Degrees", ac=True, value=gl)
    Gb = vp.Param(name="gb", ucd="pos.galactic.lat", unit="Degrees", ac=True, value=gb)

    v.What.append(vp.Group(params=[DM, DM_err, Width, SNR, Flux, Gl, Gb], name="event parameters"))

    #Advanced parameters (note, change script if using a differeing MW model)
    mw_dm = vp.Param(name="MW_dm_limit", unit="pc/cm^3", ac=True, value=ne2001)
    mw_model = vp.Param(name="galactic_electron_model", value="NE2001")
    redshift_inferred = vp.Param(name="redshift_inferred", ucd="src.redshift", unit="None", value=z)
    redshift_inferred.Description = "Redshift estimated using z = DM/1200.0 (Ioka 2003)"

    v.What.append(vp.Group(params=[mw_dm, mw_model, redshift_inferred], name="advanced parameters"))


    #WhereWhen

    vp.add_where_when(v, coords=vp.Position2D(ra=ra, dec=dec, err=errDeg, units='deg', system=vp.definitions.sky_coord_system.utc_fk5_geo),
        obs_time=datetime.datetime(utc_YY,utc_MM,utc_DD,utc_hh,utc_mm,int(utc_ss), tzinfo=pytz.UTC), observatory_location="WSRT")

    #Why
    
    vp.add_why(v, importance=imp)
    v.Why.Name = name

    if vp.valid_as_v2_0(v):
        with open('%s.xml' % name, 'wb') as f:
            voxml = vp.dumps(v)
            xmlstr = minidom.parseString(voxml).toprettyxml(indent="   ")
            f.write(xmlstr)
            print(vp.prettystr(v.Who))
            print(vp.prettystr(v.What))
            print(vp.prettystr(v.WhereWhen))
            print(vp.prettystr(v.Why))
    else:
        print "Unable to write file %s.xml" % name


if __name__ == "__main__":
    import astropy.coordinates as coord
    import astropy.units as u
    from astropy.io import ascii
    from astropy.coordinates import SkyCoord
    from astropy.time import Time
    import voeventparse as vp
    import datetime
    import os
    import sys
    import pytz
    import numpy as np
    import argparse
    from xml.dom import minidom

    parser = argparse.ArgumentParser(description="Generates a VOEvent for an FRB detected with Apertif")
    parser.add_argument('--dm', type=float)
    parser.add_argument('--dm_err', type=float)
    parser.add_argument('--width', type=float)
    parser.add_argument('--snr', type=float)
    parser.add_argument('--flux', type=float)
    parser.add_argument('--RA', type=float) #RA in degrees
    parser.add_argument('--DEC', type=float) #DEC in degrees
    parser.add_argument('--semiMaj', type=float, default=30.0) #Beam Semi-Major axis in arcminutes
    parser.add_argument('--semiMin', type=float, default=0.416) #Beam Semi-Minor axis in arcminutes
    parser.add_argument('--NE2001', type=float)
    parser.add_argument('--name', default="FRB")
    parser.add_argument('--importance', type=float, default=0.0)
    parser.add_argument('--utc', default="2018-01-01-00:00:00.0")

    if len(sys.argv[1:])==0:
        parser.print_help()
        # parser.print_usage() # for just the usage line
        parser.exit()
    args = parser.parse_args()

    dm = args.dm
    dm_err = args.dm_err
    width = args.width
    snr = args.snr
    flux = args.flux
    ra = args.RA
    dec = args.DEC
    semiMaj = args.semiMaj
    semiMin = args.semiMin
    ne2001 = args.NE2001
    name = args.name
    imp = args.importance
    utc = args.utc

    print dm, dm_err, width, flux, ra, dec, semiMaj, semiMin, ne2001, name, imp, utc

    # Parse coordinates
    c = SkyCoord(ra=ra*u.degree, dec=dec*u.degree, frame='icrs')
    g = c.galactic
    gl = g.l.deg
    gb = g.b.deg
   
    #print c, g, gl, gb
    #print utc, utc_YY, utc_MM, utc_DD, utc_hh, utc_mm, utc_ss, mjd


    NewVOEvent(dm, dm_err, width, snr, flux, ra, dec, semiMaj, semiMin, ne2001, name, imp, utc, gl, gb)
