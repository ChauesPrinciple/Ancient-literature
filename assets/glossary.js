document.addEventListener('DOMContentLoaded', function () {
    // Embedded Glossary Data (Extracted from glossary.html)
    // This approach avoids CORS issues with local file:// access
    const glossaryData = {
        "Abject": "Abject is defined as being \"brought low, miserable; craven, degraded, despicable, self-abasing.\" Abjection is a \"state of misery or degradation.\" However, these definitions are somewhat ambiguous and intangible. Thus, it is useful to consider how abjection is expressed. Religious abhorrence, incest, women's bodies, human sacrifice, bodily waste, death are examples of the abject because they are part of us but also something we wish to push away.",
        "Allegory": "A literary mode that attempts to convert abstract concepts, values, beliefs, or historical events into characters or other tangible elements in a narrative. Examples include Gulliver’s Travels, Allegory of the Cave, and Paradise Lost.",
        "Alliteration": "According to Baldick, “The repetition of the same sounds—usually initial consonants of words or of stressed syllabus—in any sequence of neighboring words” (Baldick 6). Alliteration is typically used to convey a specific tone or message.",
        "Allusion": "When a text references, incorporates, or responds to an earlier piece (including literature, art, music, film, event, etc). T.S. Eliot’s The Waste Land (1922) offers an extensive example of allusion in literature. According to Baldick, “The technique of allusion is an economical means of calling upon the history or the literary tradition that author and reader are assumed to share” (7).",
        "Anathema": "The first definition of anathema in the dictionary is a detested person or thing. Other definition of anathema is a formal ecclesiastical curse of excommunication or a formal denunciation of a doctrine. Anathema is also the person or thing so cursed.",
        "Antagonist": "A character in a text who the protagonist opposes. The antagonist is often (though not always) the villain of a story. This does not always mean that the antagonist is “bad” or “evil”, however.",
        "Apostrophe": "This figure of speech refers to an address to “a dead or absent person, or an abstraction or inanimate object” and is “usually employed for emotional emphasis, can become ridiculous [or humorous] when misapplied” (Baldick 17).",
        "Archetype": "“a resonant figure of mythic importance, whether a personality, place, or situation, found in diverse cultures and different historical periods” (Mickics 24). Archetypes differ from allegories because they tend to reference broader or commonplace (often termed “stock”) character types, plot points, and literary conventions. Paying attention to archetypes can help readers identify what an author may posit as “universal truths” about life, society, human interaction, etc. based on what other authors or participants in a culture may have said about them.",
        "Aristeia": "‘aristeia’ comes from the Greek adjective, ‘aristos,’ meaning ‘best.’ Similarly, ‘aristeuo’ means ‘to be the best.’ Following this etymology, ‘aristeia’ would mean ‘the moment of being the best,’ or ‘moment of glory.’",
        "Canto": "major division of an epic or other long narrative poem. An Italian term, derived from the Latin cantus (“song”), it probably originally indicated a portion of a poem that could be sung or chanted by a minstrel at one sitting.",
        "Catharsis": "meaning “cleansing” in Greek, refers to a literary theory first developed by the philosopher Aristotle, who believed that cleansing our emotions was the purpose of a good story, especially a tragedy. Catharsis applies to any form of art or media that makes us feel strong negative emotions, but that we are nonetheless drawn to – we may seek out art that creates these emotions because the experience purges the emotions from our system. We can feel something intense, then walk out of the theater feeling better afterwards. Catharsis is roughly synonymous with the idea of “blowing off steam.”",
        "Chivalric": "or the chivalric code, is a code of conduct associated with the medieval institution of knighthood. Chivalry arose from an idealized German custom. It developed first in the north of France among horse soldiers who served in Charlemagne′s heavy cavalry. It was originally conceived of as an aristocratic warrior code — the term derives from the French term chevalerie, meaning horse soldiery — involving gallantry, individual training, and service to others.",
        "Climax": "the highest point of tension or drama in a narrative’s plot. Often, climax is also when the main problem of the story is faced and solved by the main character or protagonist.",
        "Comitatus": "a relationship that benefited both noblemen and freemen. According to the comitatus relationship, nobleman provided the freemen with land in exchange for protection and loyalty. For freemen, it was an opportunity to rise in social status while the nobility gained protection and loyalty. Eventually, the freemen became known as thanes. The thane must agree to defend the king or nobleman to his death if necessary. In return, the nobility shared their wealth and provided weapons. Perhaps more important is the mutual respect, friendship, and honor that the nobility and thanes shared.",
        "Courtly Love": "a medieval European literary conception of love that emphasized nobility and chivalry. Medieval literature is filled with examples of knights setting out on adventures and performing various services for ladies because of their “courtly love.” This kind of love is originally a literary fiction created for the entertainment of the nobility, but as time passed, these ideas about love changed and attracted a larger audience.",
        "Cultural Area": "in anthropology, geography, and other social sciences, a contiguous geographic area within which most societies share many traits in common. Delineated at the turn of the 20th century, it remains one of the most widely used frameworks for the description and analysis of cultures.",
        "Denouement": "The “falling action” of a narrative, when the climax and central conflicts are resolved, and a resolution is found. In a play, this is typically the last act and, in a novel, it might include the final chapters.",
        "Deus Ex Machina": "According to Taafe, “Literally, in Latin, the ‘god from the machine’; a deity in Greek and Roman drama who was brought in by stage machinery to intervene in the action; hence, any character, event, or device suddenly introduced to resolve the conflict” (43).",
        "Dharma": "is the underlying nature of reality, the cosmic law that powers all things through right action. Dharma describes this immutable force, as well as the duty expected from everyone to contribute to the order of reality through that individual’s right action.",
        "Diction": "Word choice, or the specific language an author, narrator, or speaker uses to describe events and interact with other characters.",
        "Didactic": "Didacticism is a philosophy that emphasizes instructional and informative qualities in literature and other types of art. The term has its origin in the Ancient Greek word διδακτικός, \"related to education and teaching\", and signified learning in a fascinating and intriguing manner.",
        "Epithet": "According to Taafe, “An adjective, noun, or phase expressing some characteristic quality of a thing or person or a descriptive name applied to a person, as Richard the Lion-Hearted” (Taafe 58). An epithet usually indicates some notable quality about the individual with whom it addresses, but it can also be used ironically to emphasize qualities that individual might lack.",
        "Exposition": "Usually located at the beginning of a text, this is a detailed discussion introducing characters, setting, background information, etc. readers might need to know to understand the text that follows. This section is particularly rich for analysis because it contains a lot of important information in a relatively small space.",
        "Figure Fulfillment": "When one figure, image, or event, acts as a stand in for, or a promise of, a later figure, image, or event, which will fulfill the promise of the former.",
        "Foreshadowing": "gives the audience hints or signs about the future. It suggests what is to come through imagery, language, and/or symbolism. It does not directly give away the outcome, but rather, suggests it.",
        "Frame Narrative": "a story that an author encloses around the central narrative to provide background information and context. This is typically referred to as a “story within a story” or a “tale within a tale.” Frame stories are usually located in a distinct place and time from the narratives they surround. Examples of stories with frame narratives include Canterbury Tales, Frankenstein, and Hubris: the sort of pride that is so inflated that it binds, even destroys a character, even an entire people. Many characters in classical literature and Shakespeare's plays are so prideful that it destroys them; so is Satan in Milton's Paradise Lost. “like” or “as.”",
        "Hero": "A person, typically a man, who is admired or idealized for courage, outstanding achievements, or noble qualities.",
        "Heroic System": "a theory of human behavior based on the premise that the fear of death is the motivating principle of human behavior. Becker's \"ideal-real\" social science combined psychology with a mythico-religious perspective to provide a model that would insure the fullest liberation of man.",
        "Hyperbole": "exaggerated language, description, or speech that is not meant to be taken literally but is used for emphasis. For instance, “I’ve been waiting here for ages” or “This bag weighs a ton.”",
        "Imagery": "is language used by poets, novelists, and other writers to create images in the mind of the reader. Imagery includes figurative and metaphorical language to improve the reader’s experience through their senses.",
        "In media res": "Beginning in “the middle of things,” or when an author begins a text during action. This often functions to both incorporate the reader directly into the narrative and secure his or her interest in the narrative that follows.",
        "Intertextuality": "is not a literary or rhetorical device, but rather a fact about literary texts – the fact that they are all intimately interconnected. This applies to all texts: novels, works of philosophy, newspaper articles, films, songs, paintings, etc. To understand intertextuality, it’s crucial to understand this broad definition of the word “text.” Every text is affected by all the texts that came before it, since those texts influenced the author’s thinking and aesthetic choices. Remember: every text (again in the broadest sense) is intertextual.",
        "Irony": "\"A. . . perception of inconsistency, [usually but not always humorous], in which an apparently straightforward statement or event is undermined by its context so as to give it a very different significance. . . [V]erbal irony. . . involves a discrepancy between what is said and what is really meant. . . .[S]tructural irony. . . involves the use of a naive or deluded hero or unreliable narrator whose view of the world differs widely from the true circumstances recognized by the author and readers. . . . [In] dramatic irony. . . the audience knows more about a character's situation than a character does foreseeing an outcome contrary to a character's expectations, and thus ascribing a sharply different sense to the character's own statements\".",
        "Juxtaposition": "is the placement of two or more things side by side, often to bring out their differences. Imagine a man walking a well-groomed dog on a pink leash on one hand and a rough Rottweiler on a spiked collar on the other hand. The juxtaposition could be shocking, humorous, or just plain strange. Regardless, this literary term calls attention to two distinctly different things by placing them right beside one another or juxtaposing them.",
        "Karma": "(in Hinduism and Buddhism) the sum of a person's actions in this and previous states of existence, viewed as deciding their fate in future existences.",
        "Kenning": "is a figure of speech in which two words are combined to form a poetic expression that refers to a person or a thing",
        "MacGuffin": "an object or device in a movie or a book that serves merely as a trigger for the plot.",
        "Metafiction": "fiction in which the author self-consciously alludes to the artificiality or literariness of a work by parodying or departing from novelistic conventions (especially naturalism) and traditional narrative techniques.",
        "Metaphor": "a figure of speech that refers to one thing by another in order to identify similarities between the two (and therefore define each in relation to one another).",
        "Metonymy": "a figure of speech that substitutes a quality, idea, or object associated with a certain thing for the thing itself. For instance, referring to a woman as “a skirt” or the sea as “the deep” are examples of metonymy. Using metonymy can not only evoke a specific tone (determined by the attribute being emphasized or the thing to which it refers), but also comments on the importance of the specific element that is doing the substituting.",
        "Monotheistic": "defined by the Encyclopedia Britannica as belief in the existence of one God or in the oneness of God. The Oxford Dictionary of the Christian Church gives a more restricted definition: \"belief in one personal and transcendent God\", as opposed to polytheism and pantheism. A distinction may be made between exclusive monotheism, and both inclusive monotheism and pluriform monotheism which, while recognizing many distinct gods, postulate some underlying unity.",
        "Motif": "is a symbolic image or idea that appears frequently in a story. Motifs can be symbols, sounds, actions, ideas, or words. Motifs strengthen a story by adding images and ideas to the theme present throughout the narrative.",
        "Narrator": "the person telling the story, and it determines the point of view that the audience will experience. Every work of fiction has one! The narrator can take many forms—it may be a character inside the story (like the protagonist) telling it from his own point of view. It may be a completely neutral observer or witness sharing what he sees and experiences. It may be outside the story but has access to a characters or characters’ thoughts and feelings. Or it may be an all-knowing presence who knows everything about the whole story, its setting, its characters, and even all its history.",
        "Orientalism": "the representation of Asia, especially the Middle East, in a stereotyped way that is regarded as embodying a colonialist attitude.",
        "Parody": "a narrative work or writing style that mocks or mimics another genre or work. Typically, parodies exaggerate and emphasize elements from the original work to ridicule, comment on, or criticize their message.",
        "Personification": "The artistic representation of a concept, quality, or idea in the form of a person. Personification can also refer to “a person who is considered a representative type of a particular quality or concept” (Taafe 120). Many classical deities are good examples of personifications. For instance, the Greek god Ares is a personification of war.",
        "Point of View": "what the character or narrator telling the story can see (his or her perspective). The author chooses “who” is to tell the story by determining the point of view. Depending on who the narrator is, he/she will be standing at one point and seeing the action. This viewpoint will give the narrator a partial or whole view of events as they happen.",
        "Polytheistic": "the worship of or belief in multiple deities usually assembled into a pantheon of gods and goddesses, along with their own religions and rituals. It is a type of theism. Within theism, it contrasts with monotheism, the belief in a singular God. Polytheists do not always worship all the gods equally, but can be henotheists, specializing in the worship of one particular deity. Other polytheists can be kathenotheists, worshiping different deities at different times.",
        "Post Traumatic Stress Disorder": "a condition of persistent mental and emotional stress occurring because of injury or severe psychological shock, typically involving disturbance of sleep and constant vivid recall of the experience, with dulled responses to others and to the outside world.",
        "Propaganda": "a form of communication aimed towards influencing the attitude of a population toward some cause or position. Propaganda is information that is not impartial and used primarily to influence an audience and further an agenda, often by presenting facts selectively to encourage a particular synthesis or using loaded messages to produce an emotional rather than rational response to the information presented. Propaganda can be used as a form of ideological or commercial warfare.",
        "Protagonist": "The primary character in a text, often positioned as “good” or the character with whom readers are expected to identify. Protagonists usually oppose an antagonist.",
        "Redress": "to put right, esp. by compensation; make reparation for. Other definition of redress is to correct or adjust. Redress is also to make compensation to for a wrong.",
        "Satire": "The formal definition of satire is “the use of humor, irony, exaggeration, or ridicule to expose and criticize people’s stupidity or vices.” It’s an extremely broad category. The “or” in the definition is key – most satires are humorous, ironic, and exaggerated, but they only have to be one of these things to count as satire.",
        "Semiotics": "the study of signs and symbols, what they mean, and how they are used.",
        "Simile": "a figure of speech that compares two people, objects, elements, or concepts using",
        "Soliloquy": "is a kind of monologue, or an extended speech by one character. In a soliloquy, though, the speech is not given to another character, and there is no one around to hear it. Instead of another character, the soliloquy is delivered to a surrogate, to the audience, or to no one in particular.",
        "Subtext": "While not explicitly part of the plot, tx`his novel deals heavily with religious ideas and themes from both Christianity and Buddhism. They are a subtext that runs beneath the plot and influences it.",
        "Symbolic": "of or relating to a symbol or symbols. Other definition of symbolic is serving as a symbol. Symbolic is also characterized by the use of symbols or symbolism.",
        "Syncretic": "of or relating to the tendency to combine or attempt to combine the characteristic teachings, beliefs, or practices of differing systems of religion or philosophy. Other definition of syncretic is of or relating to the historical tendency of languages to reduce their use of inflection, as in the development of Old English with all its case endings into Modern English.",
        "Syndesis": "the state of being bound, linked, or connected.",
        "Themis": "(Greek: “Order”) in Greek religion, personification of justice, goddess of wisdom and good counsel, and the interpreter of the gods' will.",
        "Verisimilitude": "means ‘the quality of resembling reality.’ A work of art, or any part of a work of art, has verisimilitude if it seems realistic. The word verisimilitude is derived from the Latin words verum and similis meaning “truth” and “similar.”",
        "Zero Sum": "relating to or denoting a situation in which whatever is gained by one side is lost by the other. \"Altruism is not a zero-sum game.\""
    };

    highlightTerms(glossaryData);

    function highlightTerms(glossaryData) {
        // Sort terms by length (descending) to match longest phrases first
        const terms = Object.keys(glossaryData).sort((a, b) => b.length - a.length);

        // Exclude these tags from replacement
        const excludeTags = ['SCRIPT', 'STYLE', 'A', 'TEXTAREA', 'INPUT', 'HEAD', 'TITLE', 'META', 'LINK', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'DT', 'DD', 'BUTTON', 'OPTION', 'SELECT'];

        // Walker to traverse text nodes
        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            {
                acceptNode: function (node) {
                    if (excludeTags.includes(node.parentElement.tagName)) {
                        return NodeFilter.FILTER_REJECT;
                    }
                    if (node.parentElement.closest('.glossary-term')) {
                        return NodeFilter.FILTER_REJECT;
                    }
                    // Filter out empty or whitespace-only nodes
                    if (!node.nodeValue.trim()) {
                        return NodeFilter.FILTER_REJECT;
                    }
                    return NodeFilter.FILTER_ACCEPT;
                }
            }
        );

        const nodesToReplace = [];
        while (walker.nextNode()) {
            nodesToReplace.push(walker.currentNode);
        }

        const escapeRegExp = (string) => string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const pattern = new RegExp(`\\b(${terms.map(escapeRegExp).join('|')})\\b`, 'gi');

        nodesToReplace.forEach(node => {
            let content = node.nodeValue;

            // Quick check before expensive regex
            if (!pattern.test(content)) return;

            const fragment = document.createDocumentFragment();
            let lastIndex = 0;
            pattern.lastIndex = 0;
            let match;

            // Re-run regex to loop through matches
            while ((match = pattern.exec(content)) !== null) {
                // Text before match
                const before = content.slice(lastIndex, match.index);
                if (before) fragment.appendChild(document.createTextNode(before));

                // Match itself
                const matchedText = match[0];
                const termKey = terms.find(t => t.toLowerCase() === matchedText.toLowerCase());

                if (termKey) {
                    const span = document.createElement('span');
                    span.className = 'glossary-term';
                    span.textContent = matchedText;
                    span.dataset.term = termKey;

                    // Tooltip
                    const tooltip = document.createElement('span');
                    tooltip.className = 'glossary-tooltip';
                    tooltip.innerHTML = `<strong>${termKey}</strong><br>${glossaryData[termKey]}`;
                    span.appendChild(tooltip);

                    fragment.appendChild(span);
                } else {
                    fragment.appendChild(document.createTextNode(matchedText));
                }

                lastIndex = pattern.lastIndex;
            }

            const after = content.slice(lastIndex);
            if (after) fragment.appendChild(document.createTextNode(after));

            if (node.parentNode) {
                node.parentNode.replaceChild(fragment, node);
            }
        });

        // Mobile Support: Toggle on click
        document.body.addEventListener('click', function (e) {
            const term = e.target.closest('.glossary-term');
            if (term) {
                term.classList.toggle('active');
                // Hide others
                document.querySelectorAll('.glossary-term.active').forEach(el => {
                    if (el !== term) el.classList.remove('active');
                });
            } else {
                // Click outside, close all
                document.querySelectorAll('.glossary-term.active').forEach(el => el.classList.remove('active'));
            }
        });
    }
});
