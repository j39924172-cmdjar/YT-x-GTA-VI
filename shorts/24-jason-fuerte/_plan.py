import json
LT="../../videos/oficiales/GTAVI_Launch_Trailer.mp4"; ON="../../videos/oficiales/GTAVI_Out_Now.mp4"; PL="../../videos/oficiales/GTAVI_Pre-Load_Now.mp4"
def v(f,ini,a,b): return {"video":f,"inicio":ini,"desde":a,"hasta":b,"foco":[0.5,0.5],"zoom":[1.0,1.08]}
def im(n,a,b,foco,ff=None,z=(1.05,1.18),et=None):
    d={"img":f"capturas/{n}.jpg","desde":a,"hasta":b,"foco":foco,"foco_fin":ff or [foco[0]+0.02,foco[1]+0.02],"zoom":list(z)}
    if et: d["etiqueta"]=et
    return d
def et(t,f,fl,desde=0.2): return {"texto":t,"fondo":f,"pos":[540,1600],"desde":desde,"flecha":fl}
E=[v(LT,57.12,0,1.33), im("Jason_Duval_01",1.33,2.94,[0.74,0.4],z=(1.1,1.25)),
 im("Jason_Duval_02",2.94,5.16,[0.3,0.45],z=(1.15,1.3)),
 v(LT,7.02,5.16,7.8), v(LT,40.48,7.8,9.6),
 im("Jason_Duval_05",9.6,12.12,[0.4,0.5],z=(1.1,1.25),et=et("MORE HEALTH","amarillo",[0.3,0.35],0.4)),
 v(LT,33.68,12.12,13.46), v(LT,59.95,13.46,15.68),
 v(LT,57.12,15.68,17.0), v(LT,58.55,17.0,18.3),
 im("Leonida_Keys_01",18.3,20.4,[0.45,0.5],z=(1.05,1.25),et=et("KEY LENTO","rosa",[0.45,0.5],0.4)),
 v(LT,32.85,20.4,21.13), v(LT,10.02,21.13,22.4),
 im("Jason_Duval_01",22.4,24.6,[0.74,0.45],z=(1.25,1.1)),
 v(LT,14.25,24.6,25.47), v(LT,2.72,25.47,26.68), v(LT,55.22,26.68,28.16),
 im("Lucia_Caminos_02",28.16,30.4,[0.2,0.6],z=(1.15,1.3),et=et("FED & RESTED","amarillo",[0.12,0.62],0.4)),
 im("Brian_Heder_02",30.4,32.56,[0.65,0.5],z=(1.1,1.25)),
 im("Jason_Duval_02",32.56,34.6,[0.32,0.4],z=(1.3,1.15),et=et("TIRED?","rosa",[0.3,0.3],0.3)),
 v(ON,9.08,34.6,35.32), v(LT,47.02,35.32,36.6),
 im("Jason_Duval_18",36.6,39.0,[0.6,0.45],z=(1.1,1.25),et=et("NO TRAINING","rosa",[0.6,0.35],0.4)), v(LT,67.12,39.0,40.36),
 im("Boobie_Ike_01",40.36,41.66,[0.55,0.5],z=(1.1,1.2)),
 im("Jason_Duval_05",41.66,42.99,[0.45,0.5],z=(1.25,1.1)), v(LT,68.58,42.99,45.4),
 im("Jason_Duval_04",45.4,48.04,[0.4,0.45],z=(1.1,1.25)),
 im("Vice_City_08",48.04,51.5,[0.5,0.5],z=(1.18,1.05))]
def g(t,a,b,c,giro=False): return {"tipo":"golpe","texto":t,"desde":a,"hasta":b,"color":c,"giro":giro}
C=[{"tipo":"titulo","desde":0,"hasta":2.9,"lineas":[["WHAT IF JASON","amarillo"],["STOPS","blanco"],["TRAINING?","rosa"]],"pastilla":"GTA 6"},
 g("WEAKER",3.88,5.1,"rosa"), g("MORE HEALTH",10.84,12.0,"amarillo"), g("IT'S FREE",26.42,27.6,"amarillo"),
 g("IT DROPS",38.84,40.3,"rosa",True),
 {"tipo":"pastillas","desde":22.4,"hasta":26.0,"items":[{"texto":"WEIGHTS · BENCH","fondo":"amarillo","icono":"ok","desde":22.4,"y":760},{"texto":"PULL UPS · SQUATS","fondo":"amarillo","icono":"ok","desde":24.48,"y":880}]},
 {"tipo":"pastillas","desde":29.0,"hasta":35.2,"items":[{"texto":"FED + RESTED","fondo":"amarillo","icono":"ok","desde":29.22,"y":760},{"texto":"HUNGRY = WASTED","fondo":"rosa","color":"blanco","desde":32.56,"y":880}]},
 {"tipo":"cta","desde":48.04,"hasta":99,"lineas":["FOLLOW","FOR MORE GTA 6 SECRETS"]}]
P={"voz":"voz.mp3","palabras":"palabras.json","salida":"final.mp4","fuente":"Footage: Rockstar Games","marca":"VICECITY DAYS TV","musica":{"bpm":128,"volumen":0.3},
 "palabras_clave":["Jason","training","weaker.","strength","health,","gym","Key","Lento","free.","fed","rested,","Hungry","dropping","lifting.","Follow","secrets."],
 "escenas":E,"capas":C}
A=json.load(open("_anc.json"))
def sh(x):
    if x>=90: return x
    for (a0,b0),(a1,b1) in zip(A,A[1:]):
        if a0<=x<=a1: return round(b0+(x-a0)*(b1-b0)/(a1-a0),2)
    return round(x+A[-1][1]-A[-1][0],2)
for e in P["escenas"]:
    e["desde"]=sh(e["desde"]); e["hasta"]=sh(e["hasta"])
for c in P["capas"]:
    c["desde"]=sh(c["desde"]); c["hasta"]=sh(c["hasta"])
    for it in c.get("items",[]): it["desde"]=sh(it["desde"])
P["capas"][0]["hasta"]=2.55
for c in P["capas"]:
    if c.get("texto")=="WEAKER": c["desde"]=2.6; c["hasta"]=3.7
json.dump(P,open("plan.json","w"),indent=1,ensure_ascii=False)
