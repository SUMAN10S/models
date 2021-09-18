from flask import Flask, request
import joblib
import traceback

app = Flask(__name__)

def load_models():
  fc_model = joblib.load('./models/fc_model.joblib')
  tj_model = joblib.load('./models/tj_model.joblib')
  bp_model = joblib.load('./models/bp_model.joblib')
  ss_model = joblib.load('./models/ss_model.joblib')
  model_map = {
    'Fruit Chopper': fc_model,
    'Tower Jump': tj_model,
    'Block Puzzle': bp_model,
    'Square Stacker': ss_model,
  }
  return model_map

def load_metadata():
  fc_meta = joblib.load('./metadata/fc_meta.joblib')
  tj_meta = joblib.load('./metadata/tj_meta.joblib')
  bp_meta = joblib.load('./metadata/bp_meta.joblib')
  ss_meta = joblib.load('./metadata/ss_meta.joblib')
  meta_map = {
    'Fruit Chopper': fc_meta,
    'Tower Jump': tj_meta,
    'Block Puzzle': bp_meta,
    'Square Stacker': ss_meta,
  }
  return meta_map

model_map = load_models()
meta_map = load_metadata()

def check_valid_score(game, score, time, uid):
  if game not in model_map:
    return None
  prev_scores = meta_map[game].get(uid)
  if prev_scores==None or len(prev_scores)<5:
    avg=-1
  else:
    avg = sum(prev_scores)/5
  ratio = score/max(time, 1)
  pred = model_map[game].predict([[score, avg, ratio]])[0]
  return False if pred else True

def update_metadata(game, score, uid):
  prev_scores = meta_map[game].get(uid)
  if not prev_scores:
    meta_map[game][uid] = [score]
  if score > prev_scores[0]:
    prev_scores = prev_scores[1:] + [score]
  meta_map[game][uid] = sorted(prev_scores)


@app.route('/', methods=['POST'])
def index():
  game = request.json.get('game')
  score = int(request.json.get('score'))
  time = int(request.json.get('time'))
  uid = request.json.get('uid')
  if not all([game, score, time, uid]):
    return {'success': False, 'message': 'Arguments missing'}, 400
  try:
    res = check_valid_score(game, score, time, uid)
  except Exception as e:
    traceback.print_exc()
    return {'success': False, 'message': 'Internal Server Error'}, 500
  if res == None:
     return {'success': False, 'message': 'Game name not in list'}, 400
  if res:
    update_metadata(game, score, uid)
  return {'success': True, 'valid': res}

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
