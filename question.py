from Levenshtein import distance

class Question:
    def __init__(self, prompt, *answers):
        self.prompt = prompt
        self.answers = [x.lower() for x in list(answers)]
        self.answers.sort(key=lambda x: len(x), reverse=True)

    def how_close(self, answer):
        return [distance(answer, x) for x in self.answers]

questions = [
    Question("A room name from a typical house?", "bedroom", "living room", "kitchen", "balcony", "bathroom", "garage", "backyard"),
    Question("A family member's relation name?", "older sister", "younger sister", "older brother", "younger brother", "mommy", "mother", "mom", "momma", "mama", "father", "pop", 
        "dad", "daddy", "da", "sister", "brother", "grandpa", "grandfather", "granddad", "grandad", "grandma", "grandmother", "godfather", "godmother", "cousin", "relative", "friend"),
    Question("A thing on your desk with your computer?", "computer", "keyboard", "monitor", "cables", "cable", "headphones", "headset", "sticky notes", "sticky note", "mousepad", "desk"),
    Question("A type of clothing?", "tshirt", "tshirts", "pants", "trousers", "shirt", "shirts", "uniform", "jacket", "skirt"),
    Question("A country in Asia?", "china", "japan", "taiwan", "indonesia", "vietnam", "laos", "thailand", "bangladesh", "india", "myanmar", "brunei", "malaysia", "philippines", "north korea"
        "south korea", "mongolia", "israel", "pakistan", "iran", "iraq", "turkey", "papua new guinea", "saudi arabia", "uzbekistan", "yemen", "afghanistan", "sri lanka", "cambodia", 
        "singapore", "palestine", "nauru", "micronesia"),
    Question("A common general holiday?", "christmas", "halloween", "easter", "new year", "new year's day", "thanksgiving", ""),
    Question("A ball sport?", "baseball", "golf", "golfing", "basketball", "tennis", "badminton", "football", "soccer"),
    Question("A gaming genre?", "strategy", "rpg", "role playing game", "first person shooter", "fps", "platformer", "puzzle", "rhythm", "visual novel", "shooter", "simulation", 
        "simulator", "fighting", "casino", "tower defense", "adventure"),
    Question("A big tech company?", "apple", "google", "microsoft", "meta", "facebook", "netflix", "activision", "valve", "tencent", "cisco", "amazon", "nvidia", "bytedance", \
            "samsung", "lg"),
    Question("An operating system?", "windows", "macintosh", "mac", "linux", "openbsd", "freebsd", "android", "chromeos", "unix"),
    Question("A common dish from Japanese cuisine?", "gyoza", "sushi", "teriyaki", "takoyaki", "yakiniku", "ramen", "shirako", "udon", "mochi", "onigiri", "curry rice", "sukiyaki"),
    Question("A planet from our Solar System?", "mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"),
    Question("A subject from a school ciriculum?", "math", "mathematics", "science", "chemistry", "history", "literacy", "english", "french", "japanese", "chinese", "mandarin", \
            "spanish", "physical education", "social studies", "pe", "p.e.", "geography", "woodcutting", "music", "literature"),
    Question("A continent?", "north america", "americas", "the americas", "south america", "asia", "australia", "europe", "africa", "antarctica"),
    Question("A state from the United States?", "ohio", "detroit", "texas", "north dakota", "south dakota", "mississippi", "california", "utah", "new york", "massachusetts", \
            "illinois", "hawaii", "georgia", "alaska", "florida", "pennsylvania", "virginia", "arizona", "colorado", "north carolina", "south carolina", "michigan", "indiana", \
            "montana", "tennessee", "louisiana", "maine", "maryland", "minnesota", "oregon", "connecticut", "alabama", "wisconsin", "new mexico", "oklahoma", "kentucky", "iowa", \
            "kansa", "west virginia", "arkansas", "wyoming", "nebraska", "delaware", "vermont", "new hampshire", "idaho", "rhode island"),
    Question("Spell a number from 1-10?", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"),
    Question("A programming language?", "c", "c++", "java", "javascript", "groovy", "elixir", "rust", "python", "visual basic", "visual basic advanced", "scratch", "haskell", \
            "c#", "f#", "nim", "vimscript", "lua", "assembly", "r", "scala"),
    Question("A direction from a compass?", "southeast", "southwest", "northeast", "northwest", "north", "east", "south", "west"),
    Question("An instrument?", "bass", "bass guitar", "guitar", "cello", "viola", "violin", "piano", "grand piano", "flute", "clarinet", "organ piano", "organ", "drum"),
    Question("A common feeling name?", "happy", "sad", "angry", "mad", "sick", "excited", "unwell", "scared", "afraid", "painful"),
    Question("A very popular social media app?", "tiktok", "twitter", "youtube", "discord", "mastodon", "matrix", "reddit", "instagram", "facebook"),
    Question("A two-dimensional shape?", "square", "circle", "triangle", "rectangle", "pentagon", "hexagon", "septagon", "octagon", "nonagon", "polygon"),
    Question("A land vehicle?", "motorcycle", "scooter", "bicycle", "bike", "car", "automobile", "truck", "taxi", "legs", "golf cart", "van"),
    Question("A career profession that most children are passionate about?", "movie star", "celebrity", "influencer", "content creator", "youtuber", "tiktok star", "astronaut", "artist", \
            "programmer", "athelete", "entrepreneur", "business owner", "graphic designer", "musician", "architect", "fasion designer", "writer", "firefighter", "superhero", "biologist",\
            "doctor", "nurse", "teacher", "chef", "cook"),
    Question("Randomly state your answer in a yes/no question.", "yes", "maybe", "nope", "no", "idk", "dunno", "i dunno", "what", "prob", "probably", "yeah", "yea", "ok", "okay"),
    Question("A month name in a year?", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december")
]
