import soundfile as sf

bit_rate = 64000

ob = sf.SoundFile('Audio/from_client_original_uncompressed.wav')
print('Sample rate: {}'.format(ob.samplerate))
print('Channels: {}'.format(ob.channels))
print('Subtype: {}'.format(ob.subtype))

bit_depth = bit_rate / ( ob.samplerate * ob.channels )

print("Bit Depth: {}".format( bit_depth ) )
print("Approx. SNR: {}".format( 1.76 + (bit_depth * 6.02) ) )