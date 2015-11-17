

def increase_karma(state_dict, name):
  state_dict['karma'][name] = state_dict['karma'].get(name, 0) + 1
  return name + ": " + str(state_dict['karma'][name])

def decrease_karma(state_dict, name):
  state_dict['karma'][name] = state_dict['karma'].get(name, 0) - 1
  return name + ": " + str(state_dict['karma'][name])

def karma_all(state_dict):
  karmas = []
  for name, score in state_dict['karma'].iteritems():
    karmas.append(name + ": " + str(score))
  return "\n".join(karmas)