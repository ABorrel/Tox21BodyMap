#!/usr/bin/env Rscript
library(ggplot2)



################
#     MAIN     #
################

args <- commandArgs(TRUE)
pfilin = args[1]
pfilin = "C:/Users/Aborrel/research/NIEHS/BodyMap/RESULTS/sum_assays/count_mapping"


din = read.csv(pfilin, sep = "\t")
dcount = table(din$Type.of.organ.mapping)
dcount = cbind(names(dcount), dcount)
colnames(dcount) = c("Type_mapping", "count")
dcount = as.data.frame(dcount)
dcount$count = as.double(as.vector(dcount$count))

p = ggplot(data = dcount, aes(x=Type_mapping, y=count))+
  geom_bar(stat="identity", fill="steelblue", width = 0.9, position=position_dodge())+
  geom_text(aes(label=count), vjust=1.6, color="white", size=8)+
  labs(x="", y="Count")+
  theme(axis.title.y = element_text(size=14),axis.text.x = element_text(angle = 90, hjust = 1, size = 14), axis.text.y = element_text(size = 14))

ggsave(paste(pfilin, ".png", sep = ""),width = 6, height = 6, dpi = 300)


