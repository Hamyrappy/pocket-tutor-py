"""from metrics import bertcos

text1 = ["Hello, my dog is very cute", "Be careful, my cat can bite you"]
text2 = ["Привет, моя собака очень милая", "Осторожно, моя кошка кусается"]
print(bertcos(text1, text2))

text1 = ["Hello, my dog is very cute", "Be careful, my cat can bite you"]
text2 = [ "Осторожно, моя кошка кусается", "Привет, моя собака очень милая"]
print(bertcos(text1, text2))

text1 = ["Hello, my dog is very cute", "Be careful, my cat can bite you"]
text2 = [ "Моя корова курит травку", "Осторожно, моя коза работает в полиции"]
print(bertcos(text1, text2))"""

from app.utils.metric import cosine_similarity
from app.utils.submit import string2embedding, embedding2string, get_sentence_embedding

text1 = 'Моя корова наркоман, 12'
text2 = 'Моя собака кусается, осторожно'

pred_value = string2embedding(embedding2string(get_sentence_embedding(text1)))
gt_value = string2embedding(embedding2string(get_sentence_embedding(text2)))

if len(pred_value) != len(gt_value):
    raise ValueError(f"Embeddings have different sizes: {len(pred_value)} != {len(gt_value)}")

cos_sim_value = cosine_similarity(pred_value.unsqueeze(0), gt_value.unsqueeze(0))
cos_sim_value
float(total_cos_sim / len(true_df))