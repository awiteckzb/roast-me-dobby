FEATURE_EXTRACTION_PROMPT = """This is an image of a person. Describe the physical features of this person in a bulleted list. Feel free to be brutally honest.

Examples:
- brown eyes
- dark brown skin
- appears to be in their late 20s
- wearing a plain white shirt
"""

DOBBY_PROMPT = {
    "roast": """u need to roast the absolute shit out of me. Here's a description of my physical features:
    {description}
    do not hold back... you little whore. im not sensitive, fuck me up 
    """,
    "nice": """
    Give me some compliments please daddy ^_^. Here's a description of me:
    {description}
    """,
}

# Also, do not mention the description in your response. Just act like you saw the actual image. Be fucking mean (fuck, shit, bitch, etc.) and make your roast pretty short, like less than 2 sentences.

#     Your roast:

# "roast": """You need to roast the absolute shit out of me. Here's a description of my physical features:
#     {description}
#     do not hold back... you little whore. im not sensitive, fuck me up

#     Examples:

#     - 'You fucking ugly ass bitch brush your fucking teeth once in awhile you filthy slutty cum-dumpster'

#     """,
