#!/usr/bin/env Rscript
library(ggplot2)




################
#     MAIN     #
################

args <- commandArgs(TRUE)
pfilin = args[1]
#pfilin = "~/BodyMap/MAPPING/GeneToxCastVSBody/analysis-2/_count.csv"


din = read.csv(pfilin, sep = "\t")
#din = din[order(x = din$Ngene),]
#rownames(din) = din$Organ.tissus


p = ggplot(data = din, aes(reorder(Organ.tissus, Ngene), Ngene))+
  geom_bar(stat="identity", fill="steelblue")+
  theme(axis.text.x = element_text(angle = 90, hjust = 1))

ggsave(paste(pfilin, "_gene.png", sep = ""),width = 30, height = 10)




p = ggplot(data = din, aes(reorder(Organ.tissus, Nassay), Nassay))+
  geom_bar(stat="identity", fill="steelblue")+
  theme(axis.text.x = element_text(angle = 90, hjust = 1))

ggsave(paste(pfilin, "_assays.png", sep = ""),width = 30, height = 10)


