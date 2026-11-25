import json
LT="../../videos/oficiales/GTAVI_Launch_Trailer.mp4"; ON="../../videos/oficiales/GTAVI_Out_Now.mp4"; PL="../../videos/oficiales/GTAVI_Pre-Load_Now.mp4"
def v(f,ini,a,b): return {"video":f,"inicio":ini,"desde":a,"hasta":b,"foco":[0.5,0.5],"zoom":[1.0,1.08]}
def im(n,a,b,foco,ff=None,z=(1.05,1.18),et=None):
    d={"img":f"capturas/{n}.jpg","desde":a,"hasta":b,"foco":foco,"foco_fin":ff or [foco[0]+0.02,foco[1]+0.02],"zoom":list(z)}
    if et: d["etiqueta"]=et
    return d
def et(t,f,fl,desde=0.2): return {"texto":t,"fondo":f,"pos":[540,1600],"desde":desde,"flecha":fl}
E=[v(LT,39.05,0,1.33), v(LT,47.02,1.33,2.58),
 im("ULTIMATE_EDITION_GROTTI_CHEETAH_01",2.58,4.66,[0.5,0.55],z=(1.18,1.05)),
 v(LT,40.48,4.66,6.46), im("Vice_City_24",6.46,7.76,[0.6,0.6]),
 im("Vice_City_22",7.76,10.38,[0.55,0.65],et=et("MOSES","amarillo",[0.58,0.8],0.5)),
 im("ULTIMATE_EDITION_02",10.38,12.9,[0.5,0.6],et=et("NO TRACKER ONLY","amarillo",[0.45,0.7],1.6)),
 v(LT,26.42,12.9,14.26), v(LT,63.22,14.26,15.02),
 im("Jason_Duval_18",15.02,17.86,[0.45,0.55],et=et("TRACKED CAR","rosa",[0.42,0.68],0.6)),
 v(LT,59.95,17.86,19.24),
 im("ULTIMATE_EDITION_RIDEOUT_CUSTOMS_01",19.24,21.5,[0.5,0.5],z=(1.18,1.05),et=et("PAY 'N' SPRAY","rosa",[0.5,0.6],0.1)),
 v(LT,68.58,21.5,23.6),
 im("Raul_Bautista_02",23.6,26.0,[0.22,0.86],z=(1.15,1.3)), im("Boobie_Ike_01",26.0,27.4,[0.7,0.6],z=(1.15,1.3)),
 v(LT,33.68,27.4,28.72),
 im("ULTIMATE_EDITION_GROTTI_CHEETAH_02",28.72,31.0,[0.5,0.55],et=et("ADVANCED TRACKER","rosa",[0.5,0.6],0.8)),
 v(LT,47.02,31.0,32.74), v(LT,55.22,32.74,34.5),
 im("Vice_City_27",34.5,36.14,[0.5,0.5],z=(1.2,1.05)),
 im("ULTIMATE_EDITION_GROTTI_CHEETAH_01",36.14,38.0,[0.45,0.65],z=(1.1,1.25)), v(ON,5.25,38.0,39.28),
 im("Jason_Duval_04",39.28,41.74,[0.32,0.5],et=et("SCAN IT","amarillo",[0.31,0.52],1.2)),
 v(LT,11.95,41.74,43.78),
 v(LT,39.05,43.78,45.11), im("Vice_City_06",45.11,47.18,[0.3,0.55],z=(1.15,1.3)),
 v(PL,11.25,47.18,48.55), im("Vice_City_08",48.55,52.0,[0.5,0.5],z=(1.18,1.05))]
def g(t,a,b,c,giro=False): return {"tipo":"golpe","texto":t,"desde":a,"hasta":b,"color":c,"giro":giro}
C=[{"tipo":"titulo","desde":0,"hasta":2.5,"lineas":[["CAR TRICKS #4","amarillo"],["WHO BUYS","blanco"],["YOUR CAR?","rosa"]],"pastilla":"GTA 6"},
 g("WHO BUYS?",3.58,4.6,"amarillo"), g("REFUSED",16.82,17.8,"rosa"), g("STILL CASH",26.0,27.3,"amarillo"),
 g("RANDY",34.76,36.1,"rosa",True), g("WHO'S BUYING?",42.8,43.7,"amarillo"),
 {"tipo":"pastillas","desde":4.9,"hasta":7.7,"items":[{"texto":"3 BUYERS","fondo":"amarillo","desde":4.9,"y":760},{"texto":"3 KINDS OF CAR","fondo":"rosa","color":"blanco","desde":6.3,"y":880}]},
 {"tipo":"pastillas","desde":21.0,"hasta":23.5,"items":[{"texto":"NO TRACKER","fondo":"amarillo","icono":"ok","desde":21.28,"y":760},{"texto":"STANDARD TRACKER","fondo":"amarillo","icono":"ok","desde":22.54,"y":880}]},
 {"tipo":"cta","desde":47.18,"hasta":99,"lineas":["FOLLOW","FOR MORE GTA 6 SECRETS"]}]
P={"voz":"voz.mp3","palabras":"palabras.json","salida":"final.mp4","fuente":"Footage: Rockstar Games","marca":"VICECITY DAYS TV","musica":{"bpm":130,"volumen":0.3},
 "palabras_clave":["Stole","tracker","buys","three","Moses,","two,","no","away.","trick.","Pay","Spray","cash.","advanced","location.","one","Randy,","touch.","scan","buying?","Follow","secrets."],
 "escenas":E,"capas":C}
json.dump(P,open("plan.json","w"),indent=1,ensure_ascii=False)
