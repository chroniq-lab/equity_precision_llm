rm(list=ls());gc();source(".Rprofile")


training <- readxl::read_excel(paste0(path_equity_precision_llm_folder,"/llm training/Methods.xlsx"),sheet="Training Data")

all_abstracts <- readRDS(paste0(path_ep_folder,"/working/cleaned/epdat02_harmonized datasets.RDS")) %>% 
  dplyr::filter(!PMID %in% training$PMID)

set.seed(20241115)
development <- all_abstracts %>% 
  sample_n(size = 100)

test <- all_abstracts %>% 
  dplyr::filter(!PMID %in% development$PMID)

write_csv(development,paste0(path_equity_precision_llm_folder,"/llm training/Development Data.csv"))
write_csv(test,paste0(path_equity_precision_llm_folder,"/llm training/Test Data.csv"))
