#!/usr/bin/env Rscript
library(ggplot2)



################
#     MAIN     #
################

args <- commandArgs(TRUE)
pfilin = args[1]
pfilin = "C:/Users/Aborrel/research/NIEHS/BodyMap/RESULTS/AssaysByExp/countAssaysByExp_RefOrganExp"


din = read.csv(pfilin, sep = "\t")
din$Fold = factor(din$Fold, levels = c("Fold [2,5]", "Fold ]5,10]",  "Fold ]10", "None"))
din$Organ = factor(din$Organ, levels = rev(c("Immune System", "Nervous System", "Pituitary gland", "Skeletal Muscle", "Joint", "Uterus", "Vagina", "Ovary", "Urethra", "Mammary gland", "Testes", "Penis", "Prostate gland", "Bladder", "Placenta", "Kidney", "Adrenal gland", "Pancreas", "Stomach", "Peritoneum", "Small intestine", "Colon", "Liver", "Salivary gland", "Tongue", "Esophagus", "Lung", "Thyroid gland", "Heart", "Vascular", "Eye", "Skin", "Adipose tissue")))
  
                   

p = ggplot(data = din, aes(x=Organ, y=count, fill = Fold))+
  geom_bar(stat="identity",width = 0.9 )+#, width = 0.9, position=position_dodge())+
  #geom_text(aes(label=count), vjust=1.6, color="white", size=8)+
  labs(x="", y="Count")+
  theme(axis.title.y = element_text(size=20),axis.text.x = element_text(angle = 90, size = 14), axis.text.y = element_text(size = 14),  axis.title.x = element_text(size = 14), legend.text = element_text(size = 14), legend.title = element_text(size = 14))+
  guides(fill=guide_legend(title="Organ expression threshold (fold)"))

p + coord_flip()
ggsave(paste(pfilin, ".png", sep = ""),width = 12, height = 16, dpi = 300)

