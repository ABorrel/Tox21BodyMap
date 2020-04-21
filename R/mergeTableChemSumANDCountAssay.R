





pchemSum = "./../../RESULTS/ChemSum"
pchemAssays = "./../../RESULTS/ToxCast_prep/count_assay"


dChem = read.csv(pchemSum, sep="\t")
rownames(dChem) = dChem[,1]
dassay = read.csv(pchemAssays, sep="\t")
rownames(dassay) = dassay[,1]

lchem = intersect(rownames(dChem), rownames(dassay))

dassay = dassay[rownames(dChem),]

dChem = cbind(dChem, dassay$Assay.tested)
colnames(dChem)[dim(dChem)[2]] = "Assay.tested"
write.table(dChem, paste(pchemSum, "_clean", sep = ""), row.names = FALSE, sep = "\t", quote= FALSE)