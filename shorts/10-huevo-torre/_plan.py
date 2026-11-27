import json
LT="../../videos/oficiales/GTAVI_Launch_Trailer.mp4"; ON="../../videos/oficiales/GTAVI_Out_Now.mp4"; PL="../../videos/oficiales/GTAVI_Pre-Load_Now.mp4"
def v(f,ini,a,b): return {"video":f,"inicio":ini,"desde":a,"hasta":b,"foco":[0.5,0.5],"zoom":[1.0,1.08]}
def im(n,a,b,foco,ff=None,z=(1.05,1.18),et=None):
    d={"img":f"capturas/{n}.jpg","desde":a,"hasta":b,"foco":foco,"foco_fin":ff or [foco[0]+0.02,foco[1]+0.02],"zoom":list(z)}
    if et: d["etiqueta"]=et
    return d
def et(t,f,fl,desde=0.2): return {"texto":t,"fondo":f,"pos":[540,1600],"desde":desde,"flecha":fl}
E=[v(LT,68.58,0,1.6), im("Jason_Duval_01",1.6,3.24,[0.74,0.4],z=(1.1,1.25)),
 v(ON,5.25,3.24,4.71), v(PL,9.08,4.71,5.32),
 im("Vice_City_27",5.32,7.46,[0.55,0.45],z=(1.05,1.3),et=et("GIANT TOWERS","rosa",[0.52,0.3],0.4)),
 v(LT,63.22,7.46,8.22), v(LT,33.68,8.22,9.56),
 im("Jason_Duval_02",9.56,11.88,[0.3,0.5],z=(1.1,1.25),et=et("GIVE UP?","amarillo",[0.3,0.35],0.6)),
 v(LT,2.72,11.88,14.0), im("Vice_City_26",14.0,15.72,[0.85,0.78],z=(1.2,1.45),et=et("BIRDS UP TOP","amarillo",[0.88,0.75],0.2)),
 v(LT,55.22,15.72,17.1), v(LT,40.48,17.1,18.24),
 v(LT,32.85,18.24,18.97), v(LT,26.42,18.97,20.34),
 v(LT,59.95,20.34,21.2), v(LT,47.02,21.2,23.03),
 im("ULTIMATE_EDITION_GROTTI_CHEETAH_01",23.03,25.34,[0.4,0.6],z=(1.1,1.3),et=et("SPLAT!","amarillo",[0.36,0.6],0.6)),
 v(LT,39.05,25.34,26.67), v(PL,10.15,26.67,27.67), v(ON,9.08,27.67,28.42),
 v(LT,68.58,28.42,31.3), im("Leonida_Keys_01",31.3,34.32,[0.75,0.6],z=(1.05,1.25),et=et("THE WAY DOWN","rosa",[0.85,0.72],0.8)),
 v(LT,27.88,34.32,35.79), im("Vice_City_08",35.79,38.0,[0.5,0.5],z=(1.2,1.05)), v(LT,73.85,38.0,39.86),
 im("Jason_Lucia_Rooftop_portrait",39.86,42.2,[0.5,0.45],z=(1.0,1.12)),
 v(LT,57.12,42.2,43.53), v(PL,11.25,43.53,44.68),
 im("Jason_Duval_01",44.68,46.6,[0.74,0.4],z=(1.25,1.08)), v(LT,35.12,46.6,47.9),
 im("Grassrivers_03",47.9,50.0,[0.4,0.5],z=(1.1,1.25)), im("Vice_City_27",50.0,53.0,[0.5,0.5],z=(1.18,1.05))]
def g(t,a,b,c,giro=False): return {"tipo":"golpe","texto":t,"desde":a,"hasta":b,"color":c,"giro":giro}
C=[{"tipo":"titulo","desde":0,"hasta":3.0,"lineas":[["WHAT IF JASON","amarillo"],["THROWS AN EGG","blanco"],["OFF A TOWER?","rosa"]],"pastilla":"GTA 6"},
 g("7 MIN CLIMB",8.4,9.6,"amarillo"), g("A REAL EGG",15.72,17.0,"rosa"), g("SECRET CUTSCENE",21.32,22.7,"amarillo"),
 g("PARACHUTE",29.92,31.2,"amarillo"), g("SINCE 2002",38.48,40.0,"rosa",True),
 {"tipo":"pastillas","desde":12.3,"hasta":15.6,"items":[{"texto":"BIRD'S NEST","fondo":"amarillo","icono":"ok","desde":13.54,"y":760},{"texto":"PAINTED EGGS","fondo":"rosa","color":"blanco","desde":14.7,"y":880}]},
 {"tipo":"pastillas","desde":31.9,"hasta":34.2,"items":[{"texto":"7 MIN UP","fondo":"amarillo","desde":31.96,"y":760},{"texto":"SECONDS DOWN","fondo":"rosa","color":"blanco","desde":32.94,"y":880}]},
 {"tipo":"cta","desde":48.64,"hasta":99,"lineas":["FOLLOW","FOR MORE GTA 6 SECRETS"]}]
P={"voz":"voz.mp3","palabras":"palabras.json","salida":"final.mp4","fuente":"Footage: Rockstar Games","marca":"VICECITY DAYS TV","musica":{"bpm":128,"volumen":0.3},
 "palabras_clave":["Jason","egg","tower?","launch","seven","halfway.","nest","Easter","throw","secret","cutscene,","windscreen","parachute","twist.","2002.","Rockstar","again.","Follow","secrets."],
 "escenas":E,"capas":C}
json.dump(P,open("plan.json","w"),indent=1,ensure_ascii=False)
