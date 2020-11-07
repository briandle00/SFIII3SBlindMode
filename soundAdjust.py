def bpm_adjustment(bpm_sound, lateral_distance, base_lateral):
  if (lateral_distance == base_lateral):
    bpm_sound.stretch_factor = 1.0
  else:
    # Arbitary Numbers
    bpm_sound.stretch_factor = (2-(lateral_distance*0.002))
  return


def pitch_adjustment(pitch_sound, vert_diff):
  if (vert_diff == 0):
    pitch_sound.pitch_shift = 0
  else:
    pitch_sound.pitch_shift = 1
  return

def removeAndReset(sound, sampler):
    sound.stretch_factor = 1.0
    sound.pitch_shift = 0
    sampler.remove(sound)
    return
