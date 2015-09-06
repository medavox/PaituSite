Dynamically learning chat-bot: Ethelred
=============================
(I don't care about out how of date or mislabelled concepts are, I'm doing this FOR FUN)

Having said that, some applicable areas of CS:

* NLP
* machine learning
* Complex compound data structures


3 major parts of language:
--------------------------

* entities (or nouns)
* connections/relationships (or verbs)
* properties (or adjectives)

There are obviously other word types, but these are mostly forms of glue and special-case constructs, which may not fall under the bounds for Ethelred's dynamic learning.

Major Types of Sentence:
--------------------------

* Statement
	* makes a (possibly truthful or not; see "trustworthiness of converser") statement about something.
* Command
	* Orders to do something, ie "make me a cup of tea" or "tell me how far I am from Azerbaijan International Airport"
* Question
	* eg "What is love?"
	* Query for information; a valid fallback response is almost always "I don't know"
	* Some questions are really commands wrapped in politeness customs, ie "Can you tell me where the station is?"

further things for consideration:

* if-then constructs

Natural Language Parsing (The ULTIMATE CHALLENGE)
-------------------------------------------------

If Ethelred doesn't understand something, he can ask clarifying questions.

* If I don't turn out to be a linguistic genius and invent a general format for allowing computers to recognise patterns and similarity (lol), 
	I'll need a simpler, more specific system to spot repetition, and to prevent it in Ethelred.
* He'll need some sort of working memory of context, so if you say "I like Pizza. It tastes good", then Ethelred will know what "it" refers to.
	* Will also need to know about time, ie whether things have happened, are happening, generally are known to happen, were true but are no longer, or will be true.
	Can glean useful (but vague) time placement info from grammar.
	* This can include the repetition spotter, and also knowledge of recent topics of conversation/recent sentential subjects (ie "the man" or "the dog")
		* Conditional truth will need its own stuff.
* Could potentially build a fairly complex social network of information, ie whether bob hates joe's guts, or whether jane can generally be trusted, except when talking about music.
	* Maintaining entity information entries about conversers seems pretty solid.
	* So should trustworthiness also be topic-specific as well as converser specific? ideally, yes.


Implementation Details
----------------------

* Ethelred will be implemented as an XMPP client, AKA a 'person' you can chat with using Pidgin etc
* This means support for multiple concurrent users will be built-in (although number parallel chats will be limited by hardware; perhaps a "can we talk later, I'm too busy" response may be necessary)

I don't know yet (I really should have paid more attention is Languages & Comp, and AI...) but I think Ethelred's components will go like this:

Lexer 

Relational 

The (possibly) Clever Idea
--------------------------

* Ethelred will draw conclusions about the world based on information he is given in chat. For instance, if someone says that apples are a type of fruit, Ethelred will learn that connection. 
* Ethelred will initially be able to recognise references to previously unheard-of entities from context ("Dung beetles are smelly") (and add them to the Big list of entities he knows about), asking any necessary clarifying questions ("are "dung beetles" a thing, or are they "beetles" which are "dung")
* General hardcoded knowlede a bout english grammar will faciliate this, ie "the" or "a" generally marks the next word as a noun
* How many relationship types will need to be manually programmed in, and how many (or even whether) Ethelred will be able to infer new verbs
* Inference of new words will be helped by things like whether it contains a well-known word-class formation, eg ends in -ing or -ness or -ity or -ible.

Converser Trustworthiness
-------------------------
If Ethelred can speak to a wide range of people, then they could feed him any old misinformation, eg convince him that "squirgleblops" are a respectable form of footwear.

As such, there will need to be a trustworthiness scale for each converser. I envisage valid levels could be:-

0. Converser should not or cannot be spoken with (gibberish, another language, or some heinous crime against Ethelred)
1. Stranger: Any new thing the converser says is not be trusted, ie "I don't care if you say 'the sky' is blue, I've never heard of it."
	* Can be thought of as 'Read-only Conversation'; the converser cannot influence Ethelred whatsoever.
	* Existing known information is of course unchanged. Whether this converser corroborates is of no consequence.
2. Acquaintance: New information the converser gives needs to be checked for veracity, but is worth checking.
3. Teacher: New information is taken to be true without further checking.
	* What if a Teacher makes a statement that conflicts with existing knowledge? clarify, overwrite, ignore?
	
Higher trustworthiness users would take precedence when Ethelred is busy.

###Things that could RAISE trustworthiness of a speaker:-

* Making statements that Ethelred already knows to be true
	* Or which turn out to be true after checking with another, more trusted converser.
		* If no other conversers are available, perhaps are large number of less trusted converser
		
###Things which could LOWER the trustworthiness of a speaker:-

* Making statements Ethelred knows to be false, eg "I have 21 arms"

Other Stuff
-----------

Eventually, Ethelred will have his own "internet browser", some kind of HTTP client which presents web page text to the language engine in a sane manner, ignoring images. JavaScript support is unknown yet. Probably best to save it for later.

%tags:project,software,ai
