#!/usr/bin/env Rscript
library(ggplot2)
library(dplyr)


################
#     MAIN     #
################

args <- commandArgs(TRUE)
pfilin = args[1]
#pfilin = "C:/Users/Aborrel/research/NIEHS/BodyMap/RESULTS/sum_assays_withProp/count_mapping"


din = read.csv(pfilin, sep = "\t")

# do by prop in technology
count = summarise(group_by(din, Type.of.organ.mapping, Technology), count=n())
p = ggplot(data = count, aes(x=Type.of.organ.mapping, y=count, fill = Technology))+
  geom_bar(stat="identity",width = 0.9 )+#, width = 0.9, position=position_dodge())+
  labs(x="", y="Count")+
  theme(axis.title.y = element_text(size=20),axis.text.x = element_text(angle = 90, size = 14), axis.text.y = element_text(size = 14),  axis.title.x = element_text(size = 14), legend.text = element_text(size = 14), legend.title = element_text(size = 14))+
  guides(fill=guide_legend(title="Technology"))
ggsave(paste(pfilin, "_technology.png", sep = ""),width = 10, height = 6, dpi = 300)
write.csv(count, file=paste(pfilin, "_technology.csv", sep = ""))

# cell
count = summarise(group_by(din, Type.of.organ.mapping, Cell.types), count=n())
p = ggplot(data = count, aes(x=Type.of.organ.mapping, y=count, fill = Cell.types))+
  geom_bar(stat="identity",width = 0.9 )+#, width = 0.9, position=position_dodge())+
  labs(x="", y="Count")+
  theme(axis.title.y = element_text(size=20),axis.text.x = element_text(angle = 90, size = 14), axis.text.y = element_text(size = 14),  axis.title.x = element_text(size = 14), legend.text = element_text(size = 14), legend.title = element_text(size = 14))+
  guides(fill=guide_legend(title="Cell type"))
ggsave(paste(pfilin, "_cell.png", sep = ""),width = 16, height = 6, dpi = 300)
write.csv(count, file=paste(pfilin, "_cell.csv", sep = ""))

# tissue
count = summarise(group_by(din, Type.of.organ.mapping, Tissues), count=n())
p = ggplot(data = count, aes(x=Type.of.organ.mapping, y=count, fill = Tissues))+
  geom_bar(stat="identity",width = 0.9 )+#, width = 0.9, position=position_dodge())+
  labs(x="", y="Count")+
  theme(axis.title.y = element_text(size=20),axis.text.x = element_text(angle = 90, size = 14), axis.text.y = element_text(size = 14),  axis.title.x = element_text(size = 14), legend.text = element_text(size = 14), legend.title = element_text(size = 14))+
  guides(fill=guide_legend(title="Tissue"))
ggsave(paste(pfilin, "_tissue.png", sep = ""),width = 16, height = 6, dpi = 300)
write.csv(count, file=paste(pfilin, "_tissue.csv", sep = ""))
