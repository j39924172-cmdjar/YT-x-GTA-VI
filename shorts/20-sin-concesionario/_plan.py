import json
LT="../../videos/oficiales/GTAVI_Launch_Trailer.mp4"; ON="../../videos/oficiales/GTAVI_Out_Now.mp4"; PL="../../videos/oficiales/GTAVI_Pre-Load_Now.mp4"
def v(f,ini,a,b): return {"video":f,"inicio":ini,"desde":a,"hasta":b,"foco":[0.5,0.5],"zoom":[1.0,1.08]}
def im(n,a,b,foco,ff=None,z=(1.05,1.18),et=None):
    d={"img":f"capturas/{n}.jpg","desde":a,"hasta":b,"foco":foco,"foco_fin":ff or [foco[0]+0.02,foco[1]+0.02],"zoom":list(z)}
    if et: d["etiqueta"]=et
    return d
def et(t,f,fl,desde=0.2): return {"texto":t,"fondo":f,"pos":[540,1600],"desde":desde,"flecha":fl}
E=[v(LT,40.48,0,1.8), im("Jason_Duval_01",1.8,3.46,[0.68,0.35],z=(1.1,1.25)),
 im("Vice_City_24",3.46,5.7,[0.25,0.6],z=(1.1,1.3),et=et("NO DEALERSHIP","rosa",[0.2,0.75],0.3)),
 v(LT,26.42,5.7,7.06), v(LT,39.05,7.06,8.2), v(LT,47.02,8.2,10.03),
 im("Jason_Duval_18",10.03,12.6,[0.3,0.5],z=(1.1,1.25),et=et("NOT YOURS YET","amarillo",[0.12,0.6],0.4)),
 v(LT,59.95,12.6,13.3),
 im("ULTIMATE_EDITION_RIDEOUT_CUSTOMS_01",13.3,15.7,[0.55,0.55],z=(1.15,1.05),et=et("REGISTER IT","amarillo",[0.55,0.6],0.4)),
 v(ON,9.08,15.7,16.67), v(LT,11.95,16.67,18.52),
 im("ULTIMATE_EDITION_SAFEHOUSE_VEHICLES_01",18.52,21.2,[0.25,0.65],z=(1.1,1.3),et=et("YOUR GARAGE","rosa",[0.15,0.67],0.4)),
 v(ON,5.25,21.2,22.67), im("Vice_City_22",22.67,25.2,[0.5,0.7],z=(1.05,1.2)),
 v(PL,11.25,25.2,26.57), v(LT,63.22,26.57,27.33), v(LT,33.68,27.33,28.67),
 im("ULTIMATE_EDITION_GROTTI_CHEETAH_02",28.67,31.68,[0.5,0.55],z=(1.05,1.2)),
 im("ULTIMATE_EDITION_GROTTI_CHEETAH_01",31.68,33.9,[0.4,0.62],z=(1.1,1.25),et=et("SOMETHING SPECIAL","amarillo",[0.38,0.62],0.3)),
 v(LT,55.22,33.9,35.3),
 im("Jason_Duval_04",35.3,37.3,[0.32,0.5],et=et("SCAN IT","rosa",[0.31,0.52],0.2)),
 im("ULTIMATE_EDITION_02",37.3,39.84,[0.62,0.92],z=(1.6,1.7),et=et("NO TRACKER","amarillo",[0.6,0.85],0.6)),
 v(LT,67.12,39.84,41.2), im("Jason_Duval_01",41.2,43.2,[0.68,0.35],z=(1.25,1.1)), v(LT,68.58,43.2,45.1),
 im("Vice_City_08",45.1,49.5,[0.5,0.5],z=(1.18,1.05))]
def g(t,a,b,c,giro=False): return {"tipo":"golpe","texto":t,"desde":a,"hasta":b,"color":c,"giro":giro}
C=[{"tipo":"titulo","desde":0,"hasta":3.4,"lineas":[["WHERE DOES","amarillo"],["JASON BUY","blanco"],["CARS?","rosa"]],"pastilla":"GTA 6"},
 g("NO DEALERSHIP",4.36,5.6,"rosa"), g("STEAL IT",8.2,9.4,"amarillo"), g("CHAPTER 2",16.08,17.4,"amarillo"),
 g("ONLY 3 CARS",21.44,22.6,"rosa"), g("FIRST ONE FREE",30.4,31.6,"amarillo",True),
 {"tipo":"pastillas","desde":13.4,"hasta":18.4,"items":[{"texto":"REGISTER WITH MOSES","fondo":"amarillo","icono":"ok","desde":17.28,"y":760}]},
 {"tipo":"pastillas","desde":36.0,"hasta":39.8,"items":[{"texto":"NO TRACKER","fondo":"amarillo","icono":"ok","desde":38.94,"y":760},{"texto":"TRACKER = NO DEAL","fondo":"rosa","color":"blanco","desde":39.3,"y":880}]},
 {"tipo":"cta","desde":45.1,"hasta":99,"lineas":["FOLLOW","FOR MORE GTA 6 SECRETS"]}]
P={"voz":"voz.mp3","palabras":"palabras.json","salida":"final.mp4","fuente":"Footage: Rockstar Games","marca":"VICECITY DAYS TV","musica":{"bpm":130,"volumen":0.3},
 "palabras_clave":["Jason","Nowhere.","dealership.","steal","register","Moses.","three","garage","free.","special.","scan","tracker.","takes","Follow","secrets."],
 "escenas":E,"capas":C}
json.dump(P,open("plan.json","w"),indent=1,ensure_ascii=False)
