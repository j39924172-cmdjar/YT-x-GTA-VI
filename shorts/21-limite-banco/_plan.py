import json
LT="../../videos/oficiales/GTAVI_Launch_Trailer.mp4"; ON="../../videos/oficiales/GTAVI_Out_Now.mp4"; PL="../../videos/oficiales/GTAVI_Pre-Load_Now.mp4"
def v(f,ini,a,b): return {"video":f,"inicio":ini,"desde":a,"hasta":b,"foco":[0.5,0.5],"zoom":[1.0,1.08]}
def im(n,a,b,foco,ff=None,z=(1.05,1.18),et=None):
    d={"img":f"capturas/{n}.jpg","desde":a,"hasta":b,"foco":foco,"foco_fin":ff or [foco[0]+0.02,foco[1]+0.02],"zoom":list(z)}
    if et: d["etiqueta"]=et
    return d
def et(t,f,fl,desde=0.2): return {"texto":t,"fondo":f,"pos":[540,1600],"desde":desde,"flecha":fl}
E=[v(LT,35.12,0,1.3), im("Boobie_Ike_01",1.3,2.68,[0.7,0.6],z=(1.15,1.3)),
 v(LT,11.95,2.68,4.86), im("Lucia_Caminos_02",4.86,5.32,[0.5,0.6],z=(1.1,1.15)),
 im("Jason_Duval_04",5.32,7.96,[0.32,0.5],et=et("BUCKME APP","rosa",[0.31,0.52])),
 im("Raul_Bautista_02",7.96,10.58,[0.22,0.86],z=(1.15,1.3),et=et("PENDING","amarillo",[0.2,0.88],1.6)),
 im("ULTIMATE_EDITION_GROTTI_CHEETAH_01",10.58,12.52,[0.45,0.65],z=(1.1,1.25),et=et("SOLD CAR CASH","rosa",[0.45,0.7])),
 v(LT,47.02,12.52,13.8),
 im("Lucia_Caminos_02",13.8,15.8,[0.85,0.62],ff=[0.88,0.64],z=(1.1,1.25),et=et("BUCKME APP","rosa",[0.94,0.67],0.3)), im("Jason_and_Lucia_15",15.8,17.38,[0.25,0.7],z=(1.1,1.25),et=et("FAMILY SAVINGS","rosa",[0.19,0.74],0.1)),
 v(LT,40.48,17.38,19.18), im("Vice_City_27",19.18,21.14,[0.5,0.5],z=(1.2,1.05)),
 v(LT,26.42,21.14,22.5), v(LT,63.22,22.5,23.26), v(LT,68.58,23.26,24.96),
 v(LT,59.95,24.96,26.08),
 im("VINTAGE_VICE_CITY_WEAPON_PATTERN_01",26.08,29.44,[0.2,0.6],z=(1.1,1.3)),
 v(ON,9.08,29.44,30.41), v(LT,58.55,30.41,31.66),
 v(LT,33.68,31.66,33.0),
 im("Vice_City_06",33.0,35.4,[0.12,0.55],z=(1.15,1.3),et=et("ARRESTED","amarillo",[0.08,0.5],1.2)),
 im("Jason_Duval_18",35.4,37.4,[0.55,0.5]),
 v(LT,2.72,37.4,39.76),
 v(LT,35.12,39.76,41.06), v(ON,5.25,41.06,42.53),
 im("Boobie_Ike_01",42.53,44.18,[0.7,0.6],z=(1.3,1.12)),
 v(PL,11.25,44.18,45.55), im("Vice_City_08",45.55,49.0,[0.5,0.5],z=(1.18,1.05))]
def g(t,a,b,c,giro=False): return {"tipo":"golpe","texto":t,"desde":a,"hasta":b,"color":c,"giro":giro}
C=[{"tipo":"titulo","desde":0,"hasta":2.6,"lineas":[["MONEY TRICKS","amarillo"],["YOUR BANK","blanco"],["HAS A LIMIT","rosa"]],"pastilla":"GTA 6"},
 g("LIMIT?",2.7,4.0,"rosa"), g("PENDING",9.96,11.3,"rosa"), g("LIMIT UP",19.16,20.6,"amarillo"),
 g("NEVER COMES OUT",27.7,29.3,"rosa",True), g("CAN'T LOSE IT",32.3,33.5,"amarillo"), g("BREAK IT",43.44,44.15,"amarillo"),
 {"tipo":"pastillas","desde":17.4,"hasta":24.9,"items":[{"texto":"SAVINGS GOALS","fondo":"amarillo","icono":"ok","desde":17.76,"y":760},{"texto":"STORY CHAPTERS","fondo":"rosa","color":"blanco","desde":21.38,"y":880}]},
 {"tipo":"pastillas","desde":29.5,"hasta":31.6,"items":[{"texto":"CAN'T SPEND","fondo":"rosa","color":"blanco","desde":29.9,"y":760},{"texto":"CAN'T WITHDRAW","fondo":"rosa","color":"blanco","desde":30.84,"y":880}]},
 {"tipo":"cta","desde":44.18,"hasta":99,"lineas":["FOLLOW","FOR MORE GTA 6 SECRETS"]}]
P={"voz":"voz.mp3","palabras":"palabras.json","salida":"final.mp4","fuente":"Footage: Rockstar Games","marca":"VICECITY DAYS TV","musica":{"bpm":128,"volumen":0.3},
 "palabras_clave":["bank","limit.","BuckMe","pending.","car.","trick.","Family","Savings.","raises","limit.","story","never","Ever.","lose","die.","arrested.","trade.","more.","break","Follow","secrets."],
 "escenas":E,"capas":C}
json.dump(P,open("plan.json","w"),indent=1,ensure_ascii=False)
