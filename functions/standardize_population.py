import pandas as pd
import re

def standardize_population(value):
    if pd.isna(value) or not isinstance(value, str):
        return "Unknown"

    # Normalize case and remove extra spaces
    value = value.strip().lower()

    # List of non-human/animal, unspecified, excluded, etc. values
    excluded_values = set(["excluded", "not applicable (non-human study)", "ns", "u", "undetermined", "not applicable (study uses non-human animal models)", "not applicable (animal model study)", "not applicable (study based on cell models, not humans)", "not applicable (study is on cell lines, not humans)", "not applicable (non-human study)", "unspecified", 
                            "we (speculative)", "not applicable (study uses mice, not humans)", "not applicable (study involves yeast, not humans)", "not applicable (study uses animal models)", 
                            "not applicable (study uses animal models and in vitro analysis)", "we/na (assumed)", "not applicable (study is based on animal models)", "not applicable (animal model)", "not applicable (study uses non-human model)", 
                            "unspecified", "undetermined", "not applicable (study conducted on mouse model)", "not applicable (study involves animal models, not humans)", "not classified", "not applicable (study on rat primary hepatocytes)", 
                            "not applicable (study involves non-human animal models, wistar rats)", "not applicable (study used animal models, not human participants)", "ud", "not applicable (study conducted in rats, no human source population)", "undetermined", 
                            "na/we (assumed, but not specified)", "na/we (assumed)", "not applicable (study conducted in rat model, not humans)", "none (animal study)", "not applicable (animal and cell line study)", "not applicable (study is on dogs)", "not applicable (study involves rats, not humans)", 
                            "unspecified", "not applicable (study does not involve human subjects)", "not applicable (study on rats)", "not applicable (study conducted on mouse models)", "nd", "not applicable (study on murine models)", "not applicable (n/a, since the study involves mouse models and not human participants)", "ns", "not applicable (animal model)", 
                            "not applicable (study conducted in rats)", "not applicable (study is on rats)", "not applicable (study conducted in mice)", "not applicable (study conducted in mice)",
                            "unspecified", "exclude", "not applicable (study is based on animal models and cell cultures, not humans)", "unspecified", "not applicable (study on bovine model, not humans)", "not applicable (study on escherichia coli)", 
                            "not applicable (study based on animal models)", "not applicable (study conducted in animal models)", "non-human study", "not applicable (study based on animal models, specifically rats, and cell lines)", "not applicable (study uses non-human animal models)", "not applicable (study involves mice)", 
                            "undetermined", "n/a (non-human)", "unidentified" "not applicable (n/a, study conducted on animal model)", "not applicable (study involves animal models)", "not applicable (study conducted on non-human animals)", 
                            "unspecified", "not applicable (study conducted on animals, not humans)", "not applicable (study is in mice)", "not applicable (non-human animal study)", "not applicable (study based on non-human animal models)", "not applicable (study uses non-human models)", 
                            "not applicable (study is conducted in rats, not humans)", "not applicable (study uses mice)", "not applicable (study conducted on rat insulinoma cell line, not humans)", "ea (speculative)", "na/we (speculative)",
                            "na/we (not specified)", "not applicable (study on rats, not humans)", "not applicable (study on animal model)", "not applicable (study uses 3t3-l1 preadipocytes, which are a mouse cell line)",
                            "not applicable (study based on animal models, specifically rats, and cell lines)", "not applicable (study on bovine model, not humans)", "not applicable (study is based on animal models and cell cultures, not humans)", "exclude", "not applicable (study conducted in mice)", "not applicable (study is on rats)", "not applicable (study conducted in rats)", "ns", 
                            "not applicable (n/a, since the study involves mouse models and not human participants)", "not applicable (study on murine models)", "not applicable (study conducted on mouse models)", "not applicable (study on rats)", "not applicable (study does not involve human subjects)", "not applicable (animal and cell line study)", "not applicable (study is on dogs)", 
                            "none (animal study)", "na/we (assumed, but not specified)", "undetermined", "not applicable (study conducted in rats, no human source population)", "not applicable (study used animal models, not human participants)","not applicable (study involves non-human animal models, wistar rats)", "not applicable (study on rat primary hepatocytes)", "not applicable (study conducted on mouse model)", 
                            "unspecified", "not applicable (study is based on animal models)", "not applicable (study involves yeast, not humans)", "not applicable (study is on cell lines, not humans)", "not applicable (study uses non-human animal models)", "we/na (assumed)", "we (speculative)", "na/we (speculative)", "na/we (inferred)", "na/we (assumed)", 
                            "ea (speculative)", "ea (assumed)", "not applicable (study is based on diabetic mice models, no human population specified)", "na/we (assumed, not specified)", "not applicable (study on non-human animal model)", "not applicable (study uses a cell line, no human source population)", "na/we (not specified)", "na/we (cell line)", "unknown", "not applicable", "n/a", "N/A", "unk", 
                            "not applicable (study conducted on non-human animal models, i.e., rats)", "not specified", "Unknown", "not applicable (study uses mouse models)", "Not Applicable", "not applicable (study uses human osteosarcoma cells but does not specify human participants)", "not applicable (study conducted on mice, no human participants involved)", "Not Specified", "not applicable (study involves non-human subjects and in vitro cell models)",
                            "not applicable (animal study)", "not applicable (study in rats)", "not applicable (study conducted on rats, not humans)", "not applicable (study conducted on mice, no human source population)", "not applicable (n/a)", "not applicable (non-human animal model)", "not applicable (study based on animal model)", "ot applicable (study uses mouse models, no human population specified)", 
                            "not applicable (study uses 3t3-11 preadipocytes, which are a mouse cell line)", "indeterminate", "n/a (non-human study)", "n/a (animal study)", "not enough information", "not determinable", "not determinable (insufficient information)", "not applicable (study conducted on mice, not humans)","not applicable (study is on fish)", "not applicable (study uses cell line)", 
                            "not applicable (na)", "-", "not applicable (animal study)", "not discernible", "not applicable (study conducted in murine models)", "not applicable (study on animal models)", "not applicable (study does not involve human participants)", "none", "None", "not applicable (study uses cell lines)", "not applicable (study on plants)", "not applicable (study uses animal models, not humans)", 
                            "not determined", "non-human", "not applicable (study involves drosophila, not humans)", "not applicable (study uses murine models, not humans)", "not applicable (study conducted on animal model, rats, not humans)", "not applicable (study in mice)", "not applicable (study conducted on mice)", "not applicable (study on rabbits)", "not applicable (study on mice)", "not applicable*", 
                            "not applicable (study is on mice)", "not applicable (study involves an animal model)", "not applicable (study uses a murine model, not humans)", "not applicable (study on cell culture)", "not applicable (study on animals)", "not applicable (no human participants)", "not applicable (study involves animal models, not human participants)", "not applicable (study uses a rat model)", "[not available]", 
                            "not applicable (study conducted on mice, not humans)", "not applicable (study uses cell line)", "not applicable (study involves mouse embryonic retinal cells)", "not applicable (no specific human population identified)", "not applicable (non-human primates)", "not applicable (as the study is a review article and does not involve specific human study participants)", "not specified (n/a)", 
                            "not applicable (no human participants specified)", "no evidence due to retraction", "not applicable (study is on human cell lines, not on specific human populations)", "not applicable (study conducted in rat cell line, no human source population)", "not applicable (study on canine cells)", "not applicable (n/a, non-human study)", "not applicable (study uses a murine model)",
                            "not applicable (study uses a murine model, not human participants)", "not applicable (study uses a murine model, not human subjects)", "not applicable (study uses a murine model, not human)", "not applicable (study uses a murine model, not on humans)", "not applicable (study uses a murine model, not on human subjects)", 
                            "not applicable (study uses a murine model, not on human)", "not applicable (study uses a murine model, not on human participants)", "not applicable (study uses a murine model, not on human subjects)", "not applicable (study uses a murine model, not on human)", "not applicable (study uses a murine model, not on human subjects)", "not applicable (study involves nih3t3 cells, which are a mouse fibroblast cell line)", 
                            "not applicable (study uses raw264.7 macrophages, a murine model, thus no human source population is identified)", "not enough information to determine", "not applicable (study uses cardiac h9c2 cells, which are rat cells, not human participants)", "not assessable", "na, we (inferred, not explicit)", "und", "not applicable (n/a, as the study uses a rat model)", "mena (speculative)", "not determinable from given information", 
                            "not applicable (study on wheat)", "not applicable (study uses mouse models, not humans)", "not provided", "not applicable (study conducted on rabbits, not humans)", "not applicable (study involves non-human animal models)", "not applicable (study conducted on mice and cell lines, not humans)", "not applicable (study uses animal model)", "not applicable (study conducted on rats)", 
                            "not applicable (study conducted on cell lines, not human participants)", "not applicable (study conducted on non-human animal models)", "not identified", "not applicable (study is conducted on animal models, not humans)", "not applicable (animal models mentioned, no specific human source population)", "not applicable (study is in rat model)", 
                            "not applicable (study is on bacterial analysis and does not involve a human source population)", "tbd", "not applicable (study conducted in rats, not humans)", "not applicable (study conducted in rats, not humans)", "not applicable (study conducted in a rat model)", "not applicable (study conducted in mice, not humans)", "not applicable (study is in mouse models)", 
                            "not applicable (study is based on non-human animal models)", "not applicable (study conducted in rat cells, not humans)", "not identifiable", "not applicable (study involves mice, not humans)", "non-human animal model", "not applicable (study conducted on diabetic rats, not humans)", "not applicable (study uses model membranes, no human participants mentioned)", 
                            "not classifiable", "not applicable (study conducted in a murine model)", "not applicable (study is based on animal models, not humans)", "not applicable (study is based on rats, not humans)", "not applicable (study conducted in animal model, not humans)", "not applicable (study uses in vitro cell line)", "not applicable (study does not involve humans)", "not determinable from provided information", 
                            "not applicable (study involves murine cells, not humans)", "not applicable (study on animal models, not humans)", "n/a (insufficient information)", "not applicable (study is based on non-human animal models, specifically mice)", "not applicable (study is on animal models)", "lmics (various)", "n/a (non-human animal models)", " not applicable (study on 3t3-l1 adipocytes, an in vitro model, no human source population involved)", 
                            "not applicable (animal model used)", "not applicable (study is on non-human animal models)", "not applicable (study uses mouse models, no human population specified)", "not applicable, as the study does not involve human participants", "not applicable (study conducted on animal models, not humans)", "not applicable (study is conducted in mice, not humans)", "not applicable (study conducted on mouse cells, not humans)", 
                            "na (speculative)", "global", "not available", "not applicable (study on 3t3-l1 adipocytes, an in vitro model, no human source population involved)", "not applicable, as the study does not involve human participants.", "no information"])

    if value in excluded_values:
        return "Unknown"

    # GBD region adjustments
    region_mapping = {
        r"cee\s*or\s*mena": "mena, cee",
        r"ea\s*\(east\s*asia\)": "ea",
        r"lac\s*/\s*na": "na, lac",
        r"lac\s*/\s*we": "we, lac",
        r"na\s*/\s*we": "na, we",
        r"we\s*\(western\s*europe\)": "we",
        r"we\s*or\s*na": "we, na",
        r"na\s*or\s*we": "we, na",
        r"we\s*/\s*na": "we, na",
        r"\[?ca/cee/ea/lac/mena/seap/sa/ssa/na/we\]?": "ca, cee, ea, lac, mena, seap, sa, ssa, na, we"
    }

    # Match against region mapping
    for pattern, standardized in region_mapping.items():
        if re.fullmatch(pattern, value):
            return standardized

    # Return cleaned value if inaccurate
    return value
