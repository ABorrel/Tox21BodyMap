#!/usr/bin/env Rscript
library(ggplot2)
require(gridExtra)





################
#     MAIN     #
################

args <- commandArgs(TRUE)
pfilin = args[1]
#pfilin = "~/BodyMap/MAPPING/ToxCastVSBody/Digestive System/Cecum"

d = read.csv(pfilin, sep = "\t", header = TRUE)
rownames(d) = d[,1]
d = d[,-1]


p1 = ggplot(d, aes(x=expression)) +
  geom_histogram(aes(y=..density..), position="identity", alpha=0.35)+
  geom_density(alpha=0.3)+
  theme(text = element_text(size=19))+
  xlim(0,3000)+
  labs(title="",x="Expression", y = "Density")

p2 = ggplot(d, aes(expression, SD)) + 
  xlim(0,3000)+
  ylim(0,3000)+
  geom_point()



png(paste(pfilin, ".png", sep = ""),  width = 1200, height = 600)
grid.arrange(p1,p2,ncol=2,nrow=1)
dev.off()
