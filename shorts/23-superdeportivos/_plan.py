import json
LT="../../videos/oficiales/GTAVI_Launch_Trailer.mp4"; ON="../../videos/oficiales/GTAVI_Out_Now.mp4"; PL="../../videos/oficiales/GTAVI_Pre-Load_Now.mp4"
def v(f,ini,a,b): return {"video":f,"inicio":ini,"desde":a,"hasta":b,"foco":[0.5,0.5],"zoom":[1.0,1.08]}
def im(n,a,b,foco,ff=None,z=(1.05,1.18),et=None):
    d={"img":f"capturas/{n}.jpg","desde":a,"hasta":b,"foco":foco,"foco_fin":ff or [foco[0]+0.02,foco[1]+0.02],"zoom":list(z)}
    if et: d["etiqueta"]=et
    return d
def et(t,f,fl,desde=0.2): return {"texto":t,"fondo":f,"pos":[540,1600],"desde":desde,"flecha":fl}
E=[v(LT,47.02,0,1.83), im("ULTIMATE_EDITION_GROTTI_CHEETAH_02",1.83,3.74,[0.5,0.55],z=(1.1,1.25)),
 v(LT,59.95,3.74,4.76),
 im("ULTIMATE_EDITION_GROTTI_CHEETAH_01",4.76,7.3,[0.4,0.62],z=(1.1,1.25),et=et("LOCKED","rosa",[0.36,0.6],0.4)),
 im("Jason_Duval_04",7.3,9.5,[0.32,0.5],et=et("KEY CLONER?","amarillo",[0.31,0.52],0.2)),
 v(LT,33.68,9.5,10.84), v(LT,40.48,10.84,12.64),
 im("Vice_City_24",12.64,15.12,[0.25,0.6],z=(1.1,1.3),et=et("LOCKED BOX","rosa",[0.2,0.75],0.4)),
 v(LT,39.05,15.12,16.45), v(LT,26.42,16.45,17.81),
 im("Jason_Duval_18",17.81,19.42,[0.3,0.5],z=(1.1,1.25)),
 im("ULTIMATE_EDITION_GROTTI_CHEETAH_02",19.42,22.0,[0.5,0.55],z=(1.25,1.1),et=et("ADVANCED TRACKER","amarillo",[0.5,0.6],0.6)),
 v(LT,27.88,22.0,23.47), v(ON,9.08,23.47,24.2),
 im("Vice_City_06",24.2,27.0,[0.12,0.55],z=(1.15,1.3),et=et("COPS","rosa",[0.08,0.5],0.6)),
 v(LT,68.58,27.0,29.5), v(PL,11.25,29.5,30.87), v(LT,63.22,30.87,31.62),
 im("Jason_Duval_04",31.62,34.0,[0.32,0.5],z=(1.2,1.05),et=et("SCAN IT","amarillo",[0.31,0.52],0.4)),
 im("Vice_City_22",34.0,36.4,[0.5,0.7],z=(1.05,1.2)), v(LT,2.72,36.4,37.7),
 v(LT,55.22,37.7,39.5), v(LT,67.12,39.5,40.86),
 im("Jason_Duval_01",40.86,43.0,[0.74,0.4],z=(1.1,1.25)), v(LT,35.12,43.0,44.3),
 im("Vice_City_08",44.3,48.8,[0.5,0.5],z=(1.18,1.05))]
def g(t,a,b,c,giro=False): return {"tipo":"golpe","texto":t,"desde":a,"hasta":b,"color":c,"giro":giro}
C=[{"tipo":"titulo","desde":0,"hasta":3.6,"lineas":[["WHAT IF JASON","amarillo"],["DRIVES","blanco"],["SLOW?","rosa"]],"pastilla":"GTA 6"},
 g("TROUBLE",3.74,4.7,"rosa"), g("CHAPTER 3",9.74,10.9,"amarillo"), g("LOCKED",13.96,15.0,"amarillo"),
 g("TRACKER",21.44,22.5,"amarillo"), g("SLOW = COPS",25.96,27.4,"rosa",True),
 {"tipo":"pastillas","desde":34.9,"hasta":37.6,"items":[{"texto":"STANDARD TRACKER","fondo":"amarillo","icono":"ok","desde":35.32,"y":760},{"texto":"NO TRACKER","fondo":"amarillo","icono":"ok","desde":36.38,"y":880}]},
 {"tipo":"cta","desde":44.84,"hasta":99,"lineas":["FOLLOW","FOR MORE GTA 6 SECRETS"]}]
P={"voz":"voz.mp3","palabras":"palabras.json","salida":"final.mp4","fuente":"Footage: Rockstar Games","marca":"VICECITY DAYS TV","musica":{"bpm":130,"volumen":0.3},
 "palabras_clave":["Jason","slow?","supercar,","trouble.","Cloner,","three,","Randy.","locked","advanced","tracker.","cops","siren","WAINK","standard","heat.","Follow","secrets."],
 "escenas":E,"capas":C}
json.dump(P,open("plan.json","w"),indent=1,ensure_ascii=False)
