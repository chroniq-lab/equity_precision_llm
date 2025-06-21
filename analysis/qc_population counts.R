rm(list=ls());gc();source(".Rprofile")

library(stringr)

# Training and Development -----
training_results = read_csv(paste0(path_equity_precision_llm_folder,"/llm training/epl03_merged training data scenario 4.csv")) %>% 
  distinct(PMID,.keep_all = TRUE)

development_results = read_csv(paste0(path_equity_precision_llm_folder,"/llm training/epl03_merged development data scenario 4.csv")) %>% 
  distinct(PMID,.keep_all = TRUE)



# 2082 (incorrect) --> 2081 (duplicates) --> 2076
test_data = readxl::read_excel(paste0(path_equity_precision_llm_folder,"/llm training/epldat03_Test Data.xlsx")) %>% 
  distinct(PMID,.keep_all = TRUE)
test_results = read_csv(paste0(path_equity_precision_llm_folder,"/llm training/epl04_merged_test_data.csv")) %>% 
  distinct(PMID,.keep_all = TRUE)

test_results %>% 
  group_by(gpt_precision_medicine,gpt_diabetes,gpt_primary_study) %>% 
  tally() %>% 
  View()



# 126953 (duplicates) --> 126952
unattributable_data = read_csv(paste0(path_equity_precision_llm_folder,"/llm training/epldat03_Unattributable Data.csv")) %>% 
  distinct(PMID,.keep_all = TRUE)
unattributable_results = read_csv(paste0(path_equity_precision_llm_folder,"/llm training/epl05_merged unattributable data.csv")) %>% 
  distinct(PMID,.keep_all = TRUE)

# Exclude studies for which abstracts were not retrieved from PubMed API
table(is.na(unattributable_data$Abstract))
step2 = unattributable_results %>% 
  dplyr::filter(!is.na(Abstract)) 


# Not classified on any criteria
step3 = step2 %>% 
  group_by(gpt_precision_medicine,gpt_diabetes,gpt_primary_study) %>% 
  tally() %>% 
  View()

# Bind rows-----------

eplan01 = bind_rows(
  training_results %>% mutate(dataset = "Train"),
                    development_results %>% mutate(dataset = "Development"),
                    test_results %>% mutate(dataset = "Test"),
                    step2 %>% mutate(dataset = "Unattributable")) %>% 
  distinct(PMID,.keep_all=TRUE) %>% 
  group_by(gpt_precision_medicine,gpt_diabetes,gpt_primary_study) %>% 
  tally() 



