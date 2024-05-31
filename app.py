import streamlit as st
import openai
from pathlib import Path

# Load the OpenAI API key from Streamlit's secrets
api_key = st.secrets["api_keys"]["openai"]

def text_to_speech(text, filename, voice="alloy"):
    # Initialize the OpenAI client with the API key
    openai.api_key = api_key
    client = openai.OpenAI(api_key=api_key)
    
    # Make a request to OpenAI's TTS API to convert text to speech
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    
    # Save the audio content to a file
    speech_file_path = Path(filename)
    response.stream_to_file(speech_file_path)
    
    return filename

# Text-to-Speech Section
st.markdown("## Text-to-Speech")
st.subheader("Convert any of the story texts below to speech by copying the text and clicking convert. You can also download the result in .mp3 format.")
text = st.text_area("Enter the text you want to convert to speech:")
voice = st.selectbox("Choose a voice", ["alloy", "echo", "fable", "onyx", "nova", "shimmer"])

if st.button("Convert to Speech"):
    if text:
        with st.spinner('Generating audio...'):
            filename = "output.mp3"
            file_path = text_to_speech(text, filename, voice)
            st.audio(file_path, format='audio/mp3')
            with open(file_path, "rb") as file:
                st.download_button(
                    label="Download MP3",
                    data=file,
                    file_name=filename,
                    mime="audio/mpeg"
                )
    else:
        st.warning("Please enter some text to convert.")
        
# Function to display story
def display_story(story):
    col = st.columns(1)[0]
    with col:
        st.image(story['image'], use_column_width=True)
        st.subheader(story['title'])
        st.markdown(story['summary'])
        with st.expander("Read Full Story"):
            st.markdown(format_full_text(story['full_text']), unsafe_allow_html=True)
            audio_file = f"audio_{story['id']}.mp3"
            if st.button("Generate Audio", key=f"audio_{story['id']}"):
                with st.spinner('Generating audio...'):
                    text_to_speech(story['full_text'], audio_file, "alloy")
                st.audio(audio_file, format='audio/mp3')
                with open(audio_file, "rb") as file:
                    st.download_button(
                        label="Download MP3",
                        data=file,
                        file_name=audio_file,
                        mime="audio/mpeg"
                    )
            if st.button("Copy Text", key=f"copy_{story['id']}"):
                st.write("Text Copied!")

# Function to format the full text of the story
def format_full_text(full_text):
    paragraphs = full_text.split("\n\n")
    formatted_text = "".join([f"<p>{paragraph}</p>" for paragraph in paragraphs])
    return formatted_text

# List of stories
stories = [
    {
        "id": "story1",
        "title": "The Unlikely Hero",
        "summary": "In a galaxy torn apart by war...",
        "full_text": """The galaxy was at war. Starfleets clashed in the cold void, planets burned, and alliances crumbled. Amidst this chaos, Kira, a lowly mechanic on the barren moon of Kestris, found herself thrust into the heart of the conflict. She had always believed her life would be spent repairing starships and dreaming of adventure, but fate had other plans.\n\nOne fateful day, while scavenging for parts, Kira stumbled upon a crashed escape pod. Inside was a gravely injured alien who identified himself as Prince Thallan, heir to the Throne of Arion, a planet key to the balance of power in the galaxy. The prince carried a message of a greater threat—an ancient, malevolent force from beyond the stars, known as the Voidbringers, poised to conquer and consume all in their path.\n\nWith his dying breath, Prince Thallan entrusted Kira with a data crystal containing vital information that could unite the warring factions against the Voidbringers. Kira, never one to shirk from a challenge, vowed to honor the prince's last wish. She repaired a derelict starfighter, took the crystal, and embarked on a perilous journey.""",
        "image": "story-image1.png"
    },
    {
        "id": "story2",
        "title": "Echoes of the Future",
        "summary": "In the neon shadows of Neo-Tokyo...",
        "full_text": """In the neon-lit sprawl of Neo-Tokyo, the line between the virtual and real world had long since blurred. Megacorporations ruled with iron fists, and the city thrummed with the hum of technology and the whispers of dissent. Amidst this dystopian landscape, Jax, a rogue hacker known for his skill and audacity, stumbled upon a conspiracy that could change everything.\n\nJax had always worked alone, his only companions the countless data streams and the cold glow of his multiple monitors. One night, while navigating the dark web, he intercepted an encrypted message hinting at a project called "Echoes"—a secret program designed to control and manipulate human consciousness within the virtual world.""",
        "image": "story-image2.png"
    },
    {
    "id": "story3",
    "title": "The Clockwork Quest",
    "summary": "In the steam-powered city of Gearford, young inventor Elara and daring airship captain Gideon embark on a thrilling quest to uncover ancient technology.",
    "full_text": """In the steam-powered city of Gearford, where airships soared through smog-filled skies and clockwork mechanisms whirred tirelessly, young inventor Elara dreamed of discovery. Her life changed when she stumbled upon an ancient, forgotten map hidden within the gears of an old automaton.The map led to the lost city of Astralium, rumored to house technology far beyond their own. Elara knew she couldn't embark on this journey alone, so she sought the help of Captain Gideon, a daring airship pilot known for his unorthodox methods and unmatched skills.Together, they gathered a crew of misfits and set sail on the airship Aurora. Their quest was fraught with peril—treacherous skies, mechanical beasts, and rival treasure hunters. But Elara's ingenuity and Gideon's expertise saw them through each challenge.As they delved deeper into uncharted territories, they uncovered clues about Astralium's secrets. The lost city was said to be powered by a core of pure aetherium, a substance with limitless energy potential. Such power could revolutionize their world, but in the wrong hands, it could spell disaster.After weeks of searching, they finally reached the hidden entrance to Astralium. Inside, they found wonders beyond imagination—machines that defied the laws of physics and constructs that seemed almost alive. But they also discovered the truth: the city's downfall had been caused by the very power it sought to harness.Realizing the dangers, Elara and Gideon decided to secure the knowledge and prevent it from falling into the wrong hands. They documented their findings, disabling the most dangerous devices, and sealed the city's entrance.Returning to Gearford, they shared their discoveries, advocating for responsible use of technology. Elara's reputation as an inventor soared, and Gideon became a legend. Together, they inspired a new era of innovation tempered with caution, ensuring the mistakes of Astralium would never be repeated.""",
    "image": "story-image3.png"
},
{
    "id": "story4",
    "title": "The Hidden Underworld",
    "summary": "Detective Lila Blake navigates the hidden underworld of New Avalon, where magical creatures and wizards dwell alongside humans.",
    "full_text": """In the bustling metropolis of New Avalon, Detective Lila Blake was known for her sharp mind and unyielding determination. However, few knew that Lila had a secret—she was one of the few humans aware of the city's hidden underworld, a realm of magical creatures and ancient wizards existing alongside the mundane world.
Her dual knowledge came into play when a series of bizarre crimes began to plague New Avalon. Victims were found with strange, arcane symbols etched into their skin, and the air was thick with dark magic. Lila knew this wasn't the work of any ordinary criminal.
Using her connections in both worlds, Lila began her investigation. She consulted with Finn, a centuries-old wizard, and Delilah, a shapeshifter with a penchant for secrets. Together, they uncovered a sinister plot orchestrated by a rogue mage seeking to merge the magical and human realms by breaking the ancient barriers that separated them.
As the crimes escalated, Lila's two worlds collided. She had to navigate treacherous alliances and fend off magical attacks, all while keeping the truth hidden from her colleagues in the police force. The stakes were raised when the rogue mage kidnapped Delilah, intending to use her unique abilities to finalize the ritual.
In a race against time, Lila and Finn confronted the rogue mage in an abandoned cathedral, the epicenter of magical convergence. The battle was fierce, spells clashing and energy crackling in the air. Just as the mage began the final incantation, Lila, using a combination of wit and courage, disrupted the ritual, freeing Delilah and neutralizing the mage.
With the threat averted, the barriers between the worlds remained intact. Lila ensured the rogue mage was imprisoned in the magical realm, unable to threaten either world again. Her actions earned her respect in both realms, but she knew her work was far from over.
New Avalon thrived, with its secret underworld continuing to coexist in the shadows. And Detective Lila Blake stood as its silent guardian, ever vigilant against the dark forces that threatened the delicate balance.""",
    "image": "story-image4.png"
},
{
    "id": "story5",
    "title": "The Quest for the Crystal",
    "summary": "In the realm of Eldoria, darkness rises as the Dark Sorcerer Malakar seeks to conquer the land.",
    "full_text": """In the ancient realm of Eldoria, where dragons soared through the skies and mythical creatures roamed the forests, a shadow of darkness began to spread. The Dark Sorcerer, Malakar, had risen, seeking to plunge the land into eternal night. The only hope lay in the legendary Crystal of Light, hidden deep within the heart of the Forbidden Mountain.A prophecy foretold that only a band of true-hearted adventurers could retrieve the crystal and save Eldoria. Thus, a diverse group was assembled: Eamon, a valiant knight; Lyra, a skilled archer; Thorne, a cunning rogue; and Arin, a young mage with untapped potential.
Their journey was fraught with peril. They crossed treacherous landscapes, battled fierce creatures, and solved ancient riddles. Along the way, they forged an unbreakable bond, each bringing their unique strengths to the fore. Eamon's bravery, Lyra's precision, Thorne's agility, and Arin's growing magical prowess complemented each other perfectly.
As they neared the Forbidden Mountain, Malakar's minions attacked in full force. The adventurers fought valiantly, but the dark magic was overwhelming. In a moment of desperation, Arin tapped into a hidden well of power, casting a spell that drove the minions back and revealed the entrance to the mountain.
Inside, they faced the final challenge: a labyrinth filled with traps and illusions. Their unity and trust in each other saw them through, leading them to the chamber of the Crystal of Light. As they approached, Malakar himself appeared, wielding dark sorcery.
The battle was fierce, with the very fate of Eldoria hanging in the balance. Just when all seemed lost, Eamon's courage, Lyra's arrows, Thorne's stealth, and Arin's magic combined in a final, desperate strike. The crystal unleashed a blinding light, vanquishing Malakar and dispelling the darkness.
With the Dark Sorcerer defeated, the realm of Eldoria was saved. The adventurers returned as heroes, their names forever etched in legend. The Crystal of Light was placed in the capital, a symbol of hope and unity.
Eldoria flourished, and the bond between the adventurers remained strong. They had not only saved their world but also proven that even in the darkest times, light and unity could prevail.""",
    "image": "story-image5.png"
}

# Streamlit App Layout
st.title("Fast AI Fiction")

# Custom CSS for responsive layout
st.markdown("""
    <style>
    .story-card {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;
    }
    .story-card > div {
        flex: 0 1 30%;
        margin: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Display stories
st.markdown('<div class="story-card">', unsafe_allow_html=True)
for story in stories:
    display_story(story)
st.markdown('</div>', unsafe_allow_html=True)



