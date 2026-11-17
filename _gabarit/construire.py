"""Construit la page d'un QCM distanciel à partir du gabarit.

Usage : python3 construire.py <dossier_source> <nom_du_qcm> "<classe>" <duree_min>
  <dossier_source> contient questions.json (sans les réponses : le corrigé reste sur le Mac).
  La page est écrite dans ~/qcm-distanciel/<nom_du_qcm>/index.html.
"""
import json, os, sys, html

src, nom, classe, duree = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
URL = "https://script.google.com/macros/s/AKfycbxU63Rmn3UOkGhpRNDfG_GINqkU7ZtphjAKs_NfNrnMplj5LNS-_132jVJS9V8ERxpx/exec"

data = json.load(open(os.path.join(src, "questions.json"), encoding="utf-8"))
questions = [{"n": q["n"], "texte": q["texte"], "propositions": q["propositions"]} for q in data["questions"]]
assert all("reponse" not in q and "bonne" not in q for q in questions), "le corrigé ne doit pas être dans la page"

config = {"qcm": nom, "classe": classe, "titre": data["titre"], "duree_min": duree, "url": URL, "questions": questions}
gabarit = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gabarit.html"), encoding="utf-8").read()
page = (gabarit.replace("__TITRE__", html.escape(data["titre"]))
               .replace("__CONFIG__", json.dumps(config, ensure_ascii=False).replace("</", "<\\/")))
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), nom)
os.makedirs(out, exist_ok=True)
open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(page)
print("écrit :", os.path.join(out, "index.html"))
