
# from https://huggingface.co/datasets/pile-of-law/pile-of-law/blob/main/pile-of-law.py
DATA_URL = {
    "r_legaladvice" : 
    {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.r_legaldvice.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.r_legaldvice.jsonl.xz"]
    },
    "courtlistener_docket_entry_documents" : {
        "train" : [
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.courtlistenerdocketentries.0.jsonl.xz",
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.courtlistenerdocketentries.1.jsonl.xz",
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.courtlistenerdocketentries.2.jsonl.xz",
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.courtlistenerdocketentries.3.jsonl.xz"
        ],
        "validation" : [
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.courtlistenerdocketentries.0.jsonl.xz",
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.courtlistenerdocketentries.1.jsonl.xz"
        ]
    },
    "atticus_contracts" : {
        "train" : [
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.atticus_contracts.0.jsonl.xz",
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.atticus_contracts.1.jsonl.xz",
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.atticus_contracts.2.jsonl.xz",
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.atticus_contracts.3.jsonl.xz",
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.atticus_contracts.4.jsonl.xz"            
        ],
        "validation" : [
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.atticus_contracts.0.jsonl.xz",
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.atticus_contracts.1.jsonl.xz"
        ]
    },
    "courtlistener_opinions" : {
        "train" : [
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.courtlisteneropinions.0.jsonl.xz",
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.courtlisteneropinions.1.jsonl.xz",
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.courtlisteneropinions.2.jsonl.xz",
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.courtlisteneropinions.3.jsonl.xz",
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.courtlisteneropinions.4.jsonl.xz",
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.courtlisteneropinions.5.jsonl.xz",
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.courtlisteneropinions.6.jsonl.xz",
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.courtlisteneropinions.7.jsonl.xz",
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.courtlisteneropinions.8.jsonl.xz",
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.courtlisteneropinions.9.jsonl.xz",

        ],
        "validation" : [
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.courtlisteneropinions.0.jsonl.xz",
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.courtlisteneropinions.1.jsonl.xz",
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.courtlisteneropinions.2.jsonl.xz",
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.courtlisteneropinions.3.jsonl.xz"
        ]
    },
    "federal_register" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.federal_register.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.federal_register.jsonl.xz"]
    },
    "bva_opinions" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.bva.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.bva.jsonl.xz"]
    },
    "us_bills" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.us_bills.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.us_bills.jsonl.xz"]
    },
    "cc_casebooks" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.cc_casebooks.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.cc_casebooks.jsonl.xz"]
    },
    "tos" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.tos.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.tos.jsonl.xz"]
    },
    "euro_parl" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.euro_parl.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.euro_parl.jsonl.xz"]
    },
    "nlrb_decisions" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.nlrb_decisions.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.nlrb_decisions.jsonl.xz"]
    },
    "scotus_oral_arguments" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.scotus_oral.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.scotus_oral.jsonl.xz"]
    },
    "cfr" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.cfr.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.cfr.jsonl.xz"]
    },
    "state_codes" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.state_code.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.state_code.jsonl.xz"]
    },
    "scotus_filings" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.scotus_docket_entries.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.scotus_docket_entries.jsonl.xz"]
    },
    "bar_exam_outlines" : {
        "train" : [
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.stanfordbarexamoutlines.jsonl.xz",
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.shajnfeldbarexamoutlines.jsonl.xz",
        ],
        "validation" : [
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.stanfordbarexamoutlines.jsonl.xz",
            "https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.shajnfeldbarexamoutlines.jsonl.xz",
        ]
    },
    "edgar" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.edgar.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.edgar.jsonl.xz"]        
    },
    "cfpb_creditcard_contracts" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.cfpb_cc.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.cfpb_cc.jsonl.xz"]        
    },
    "constitutions" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.constitutions.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.constitutions.jsonl.xz"]        
    },
    "congressional_hearings" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.congressional_hearings.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.congressional_hearings.jsonl.xz"]        
    },
    "oig" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.oig.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.oig.jsonl.xz"]        
    },
    "olc_memos" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.olcmemos.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.olcmemos.jsonl.xz"]        
    },
    "uscode" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.uscode.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.uscode.jsonl.xz"]        
    },
    "founding_docs" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.founding_docs.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.founding_docs.jsonl.xz"]        
    },
    "ftc_advisory_opinions" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.ftc_advisory_opinions.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.ftc_advisory_opinions.jsonl.xz"]        
    },
    "echr" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.echr.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.echr.jsonl.xz"]        
    },
    "eurlex" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.eurlex.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.eurlex.jsonl.xz"]        
    },
    "tax_rulings" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.taxrulings.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.taxrulings.jsonl.xz"]        
    },
    "un_debates" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.undebates.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.undebates.jsonl.xz"]        
    },
    "fre" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.fre.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.fre.jsonl.xz"]      
    },
    "frcp" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.frcp.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.frcp.jsonl.xz"]      
    },
    "canadian_decisions" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.canadian_decisions.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.canadian_decisions.jsonl.xz"]     
    },
    "eoir" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.eoir.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.eoir.jsonl.xz"]     
    },
    "dol_ecab" : {
        "train" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/train.dol_ecab.jsonl.xz"],
        "validation" : ["https://huggingface.co/datasets/pile-of-law/pile-of-law/resolve/main/data/validation.dol_ecab.jsonl.xz"]     
    }
}
