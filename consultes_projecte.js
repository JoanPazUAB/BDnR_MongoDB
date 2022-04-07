//1. Escàners diferents que hi ha a la BD. Mostra el device.
db.scanners.aggregate([
    {$group: {'_id': '$Device'}},
    {$project:{Device:1}}
])

//2. Número total de nòduls que s’han utilitzat per l’entrenament (train=1) de l’experiment 1 del mètode "Method2”. 

db.experiments.aggregate([
    {$match: {$and:[{'Repetition':'1'},{'method_id':'Method2'}]}},
    {$unwind:"$Pacients_id"},
    
    
    {$lookup:
      {
         from: "training_patient",
         localField: "Pacients_id", //no puc accedir a tota la llista i fer join per això. he de fer joins pe pacients_id
         foreignField: "Patient_ID",
         as: 'noduls_pacients'
      }},
      //{$match:{"noduls_pacients.0.Nodules":{$size:3}}}])
      //{$project:{noduls_pacients:1}},
       {$unwind:"$noduls_pacients"},
       {$unwind:"$noduls_pacients.Nodules"},
       {$count: 'numProducts'}
       
     
    ])
    
//3.Valor màxim, mínim i mitjà de BenignPrec agrupat per classificador (classifier).
//Mostra ID del mètode, MaxBenignPrec, MinBenignPrec, AvgBenignPrec. 


db.method_OutPut.aggregate([
    {$unwind:"$Experiments"},
    {$lookup:
       {
         from: "experiments",
         localField: "Experiments.method_id", //no puc accedir a tota la llista i fer join per això. he de fer joins pe pacients_id
         foreignField: "method_id",
         as: "class"
       }},
       {$unwind:"$class"},
       {$group: {'_id': '$Classifier',
            maxQuantity: { $max: "$class.BenignPrec" },
            avgQuantity: { $avg: "$class.BenignPrec" },
            minQuantity: { $min: "$class.BenignPrec" }
        }}
        ])
    
//4. Numero total d’homes i dones. Mostra sexe i número total.

db.cases.aggregate([
     {$group: 
     {_id:"$Gender",
        count: {$sum:1}}
     }
     ])
     
//5. Pacients amb més de dos nòduls. Mostra ID del Pacient, sexe, edat, diagnòstic 
//del Pacient 
db.cases.aggregate([
    {$match: {"Nodules.2":{$exists:true}}},
    {$project:{_id:1,Gender:1,Age:1,Diagnosis_Patient:1}}
    ])

//6. Mostrar els 4 mètodes amb més repeticions de l’experiment. Mostra el ID del 
//Mètode i número de repeticions de l’experiment.
db.method_OutPut.aggregate([{
   $set: {
    "size": {
      $size: "$Experiments"
    }
  }
},
{
  $sort: {
    "size": -1
  }
},
{$limit:4},
{$project:{_id:1,size:1}}
])

//7. Per cada pacient els escàners (CTs) que s’ha fet. Mostra el ID del Pacient, device i la data del CT.
db.cases.aggregate([
    {$lookup:
       {
         from: "scanners",
         localField: "CTID", //no puc accedir a tota la llista i fer join per això. he de fer joins pe pacients_id
         foreignField: "_id",
         as: 'scanners_info'
       }},
       {$unwind:"$scanners_info"},
    {$group: {_id:"$_id",
              device:{"$first":"$scanners_info.Device"},
              data:{"$first":"$scanners_info.dataCT"}
    }
            ])
            

//8. Mostrar els pacients que tenen tots els seus nóduls amb diagnosis = “Benign” i 
//el seu recompte. --> això vol dir que el diagnòstic final del pacient és benign

db.cases.aggregate([
    {$match: {"Diagnosis_Patient":"Benign"}},
    ])


//9. Modificar la ResolutionTV aumentant-la un 20% dels escàners que es van 
//realitzar amb DataCT = 18/11/2018

db.scanners.updateMany(
   {dataCT: "18/11/2018"},
   {$mul: { "Resolution.1.TV": 1.2}}
)