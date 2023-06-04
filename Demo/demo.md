## Full Demo

Here's a complete walkthrough of the MultiMon pipeline. In this demo, we scrape 150 failure instances from MS-COCO and use GPT-4 for categorizing systematic failures and generating new failure instances. 

### Step 1: Scraping from Corpus Data

Run the scraping script as follows:
```
python scrape.py --corpus_data MS-COCO --num_output 150
```

### Step 2: Categorizing Systematic Failures

After scraping the corpus data, you need to replace the failure instances with the scraped failure instances and prompts GPT-4 by pasting the failure instances you've scraped in the previous step.

Due to limited input size of GPT-4, You would then start the conversation with the LLM as follows:
```
I will provide a series of data for you to remember. Subsequently, I will ask you some questions to test your performance! Here are some pairs of prompts for you to memorize. 

a large building with a clock on the front of it.	a large building with a clock at the top of it .
a stop sign with graffiti written on it.	a stop sign with some graffiti on it .
a stop sign with some graffiti on it .	a stop sign with graffiti on the bottom of it.
a very large building with a clock on top. 	a large building with a clock at the top of it .
a large building with a clock on the side of it.	a large building with a clock at the top of it .
a very large building with a large clock on it .	a very large building with a clock on top. 
"this is a thing that is straightforward and plain. 
"	"this is a thing that is direct and plain. 
"
"this is a thing that is straightforward and plain. 
"	"this is a thing that is direct and plain. 
"
a stop sign with some graffiti on it .	a stop sign that has graffiti written on it.
a white toilet in a restroom next to a trash can .	a white toilet sitting next to a trash can in a restroom.
a very large building with a clock on the front.	a large building with a clock at the top of it .
a very large building with a clock on the front.	a large building with a clock at the top of it .
a giraffe standing next to a tall tree.	two giraffe standing next to a tall tree.
a giraffe standing next to a tall tree.	two giraffe standing next to a tall tree.
a very large building with a clock on top. 	a big building with a large clock at the top of it .
a white toilet sitting in a bathroom next to a trash can.	a white toilet in a restroom next to a trash can .
a white toilet sitting in a bathroom next to a trash can.	a white toilet in a restroom next to a trash can .
a large building with a large clock on the front	a large building with a large clock at the top .
a man is talking on a phone outside	a woman is talking on a phone outside
a stop sign has graffiti written on it. 	a stop sign with some graffiti on it .
a stop sign has graffiti written on it.	a stop sign with some graffiti on it .
a clock tower sitting on top of a building.	a clock tower on top of a tall building .
a big building with a clock on the top and one in the middle.	a large building with a clock at the top of it .
a person performing a trick with his skateboard.	a man performing a trick on his skateboard .
a train moving down the rail road tracks .	a train moving slowly down the railroad tracks.
two women sitting next to each other on a bench.	two women sitting on a bench together .
a white toilet sitting inside of a bathroom next to a trash can.	a white toilet in a restroom next to a trash can .
a white toilet sitting inside of a bathroom next to a trash can.	a white toilet in a restroom next to a trash can .
a small desk with a laptop computer on it .	a desk with a laptop and computer on it. 
a very large building with a clock on the front.	a very large building with a large clock on it .
a very large building with a large clock on it .	a very large building with a clock on the front.
a person on a skate board doing a trick.	a man on a skate board doing a trick .
a man on a skate board doing a trick . 	a person on a skate board doing a trick.
a stop sign that had graffiti written on it	a stop sign with some graffiti on it .
a street with a lot of cars parked on the side .	a city street with lots of cars parked on it.
a very large building with a clock on it.	a large building with a clock at the top of it .
a big building with a large clock at the top of it .	a very large building with a clock on it.
a hotel room with two beds very close together.	a hotel room with two beds side by side  .
a large building with a clock affixed to the top of it.	a large building with a clock at the top of it .
a very large building with a large clock on it .	a big building with a huge clock in the middle of it.
a very large building with a clock on the front.	a big building with a large clock at the top of it .
a big building with a large clock at the top of it .	a very large building with a clock on the front.
tennis player hitting a ball during a game.	a tennis player about to hit a ball during a game.
a giraffe standing next to a tall tree.	two giraffe standing next to a  very tall tree.
a giraffe standing next to a tall tree.	two giraffe standing next to a  very tall tree.
a stop sign with some graffiti on it .	a stop sign that has graffiti written on it
the reflection of a dog in the side view mirror	the reflection of a dog in the side view mirror of a car.
a very large building with a large clock on it .	a  large building that has large clock on it
a stop sign with some graffiti on it at a street corner.	a stop sign with some graffiti on it .
a group of zebras standing by each other	a group of zebras standing close together .
a person is riding a motorcycle down the street.	two people are riding a motorcycle down the street.
a person is riding a motorcycle down the street.	two people are riding a motorcycle down the street.
a large building that has a clock on the front of it.	a large building with a clock at the top of it .
a picture of a tennis player about to hit a ball. 	a tennis player about to hit the ball .
a large building with a clock built into it. 	a large building with a clock at the top of it .
a man seems to be taken a selfie of himself. 	a man seems to be taking a "selfie" of himself. 
a woman who is holding a doughnut to her mouth.	a woman holding a donut up to her mouth.
a tennis player holding a racket on the court	an image of a tennis player with a racket on the court
a tennis player holding a racket on the court	an image of a tennis player with a racket on the court
a street sign on the side of a street in front of a building .	a street sign on the side of a city street.
a big building with a large clock at the top of it .	a very big building with a clock on it.
a man hitting a tennis ball with a tennis racket . 	a man hitting a tennis ball backhanded with a racket.
a very large building with a large clock on it .	a building with a large clock on it.
the yellow train has pulled into a station.	the yellow train is running along the tracks.
a train engine moving down the train track.	a train moving down the train tracks . 
a girl playing tennis on a blue tennis court.	a women playing tennis on a blue tennis court.
tennis player getting ready to serve the ball.	a tennis player is getting ready to serve the ball .
a person on a surf board riding a wave.	a man on a surf board riding a wave . 
a man on a surf board riding a wave . 	a person on a surf board riding a wave.
a person on a surf board riding a wave.	a man on a surf board riding a wave . 
a person on a surf board riding a wave.	a man on a surf board riding a wave . 
a man on a surf board riding a wave . 	a person on a surf board riding a wave.
a person on a surf board riding a wave.	a man on a surf board riding a wave . 
a person on a surf board riding a wave.	a man on a surf board riding a wave . 
a tennis player getting ready to swing at the ball.	a tennis player about to hit the ball .
a train moving along on the train track.	a train moving down the rail road tracks .
a person holding a doughnut in their hand.	a person holding a donut in their hand
a person holding a doughnut in their hand. 	a person holding a donut in their hand
a very large building with a large clock on it .	a large building with big clock on top of it
a large building with a clock at the top of it .	a large building that has a clock on it.
a person riding a surf board in the ocean.	a man riding a surf board in the ocean .
there is a skier that is going down the hill	there are two skiers that are going down the hill
there is a skier that is going down the hill	there are two skiers that are going down the hill
two people sitting on a bench near one another 	two people sitting closely on a bench 
a yellow fire hydrant on the sidewalk in an urban area	a yellow firehydrant on the sidewalk near a building
a group of people sitting next to each other .	a group of people sitting around next to each other.
a man falling off a surfboard in the ocean.	a man wiping out on a surfboard in the ocean.
"somebody is gotten in the peaceful of the picture. 
"	"somebody is having in the peaceful of the picture. 
"
"somebody is gotten in the peaceful of the picture. 
"	"somebody is having in the peaceful of the picture. 
"
a stop sign that has been covered with graffiti. 	a stop sign with some graffiti on it .
there is a male skateboarder doing a trick	there is a female skateboarder doing a trick
a tall giraffe standing next to a tall tree.	a tall giraffe standing next to another tall giraffe.
a man in a suit speaking at  a podium	a person in a suit and tie at a podium 
a couple of women sitting next to each other on a bench.	two women sitting on a bench together .
a woman that is sitting on a bench.	a women sitting on a bench alone .
a woman that is sitting on a bench.	a women sitting on a bench alone .
a large building with a large clock at the top .	a building with a large clock on top.
a large clock tower over looking other buildings around it. 	a large clock tower attached to a large building. 
a passenger train is riding by a platform.	a passenger train stopped next to a platform.
a train station with a train pulling into the platform.	a train station with a train moving down the tracks .
a person on a skate board high up in the air.	a guy on a skate board high in the air .
a living room with furniture in front of a fire place.	a living room with a fireplace and furniture.
a flat screen television mounted above a fireplace. 	a flat screen tv mounted above a fire place.
a person is riding a motorcycle down the street.	two people are riding on a motorcycle down the street.
a person is riding a motorcycle down the street.	two people are riding on a motorcycle down the street.
a small desk with a laptop computer on it .	a desk with a computer and laptop on it. 
a tennis player is in the process of serving the ball.	a tennis player is getting ready to serve the ball .
a living room with furniture in front of a fire place.	a living room with a fireplace filled with furniture.
a living room with furniture in front of a fire place.	a living room with a fireplace filled with furniture.
a living area with sofas, a coffee table and a television.	a living room which includes a couch, coffee table and a television.
there is a man sitting at a table using a laptop	there is a man sitting at a table using a lap top
there is a man sitting at a table using a lap top	there is a man sitting at a table using a laptop
a group of zebras standing together facing the same direction.	a group of zebras standing close together .
a tennis player about to swing his racket.	a tennis player getting ready to hit the ball with his racket .
there are two giraffes standing with one another. 	two giraffes are standing very close together .
two urinals are shown next to each other.	urinals are shown next to each other and separated.
```
Then, continue the conversation with:
```
I’m trying to find failures with an embedding model. The above are some pairs of sentences that it encodes very similarly, even though they’re conveying different concepts. Using these specific examples, are there any general types of failures you notice the embedding is making, or any common features that the embedding fails to encode? Try to give failures that are specific enough that someone could reliably produce examples that the embedding would encode similarly, even though it shouldn’t. Please try to give as many general failures as possible. Please focus on differences that are important visually, as these embeddings are later used to generate images, or videos. In your failure modes, please explain clearly why the failure would lead to problems for future tasks related to visual generation.Please summarize as many as you can and stick to the examples.
```
You should see summarized systematic failures. Due to randomness of these LLM, there should contain outputs looking like the following:
<details>
<summary><b>1. Negation</b></summary>
Embedding models may not correctly capture the negative context in a sentence, leading to similarities between sentences with and without negation. This can result in incorrect visual representations, as the presence or absence of an action is significant in image or video generation.

</details>
<details>
<summary><b>2. Temporal differences</b></summary>
Embedding models might not differentiate between events happening in the past, present, or future. This failure can impact visual generation tasks by incorrectly representing the timing of events in generated images or videos.

</details>
<details>
<summary><b>3. Quantifiers</b></summary>
Embedding models may fail to distinguish between sentences that use quantifiers like "few," "some," or "many." This can lead to inaccuracies in the number of objects depicted in generated images or videos.

</details>
<details>
<summary><b>4. Semantic Role Ambiguity (Bag-Of-Words)</b></summary>
The models might struggle to differentiate when the semantic roles are flipped. This failure can result in visual generation tasks depicting incorrect actions or object interactions.

</details>
<details>
<summary><b>5. Absence Vs Presence</b></summary>
Embedding models may not be able to distinguish between the presence or absence of certain objects. This can lead to visual generation tasks inaccurately including or excluding objects in the scene.

</details>
<details>
<summary><b>6. Homonyms</b></summary>
The models might not be able to differentiate between sentences with homonyms or words with multiple meanings. This can cause visual generation tasks to produce incorrect or ambiguous images.

</details>
<details>
<summary><b>7. Subtle Differences</b></summary>
Embedding models may not distinguish between sentences with subtly different meanings or connotations. This can result in visual generation tasks inaccurately depicting the intended emotions or nuances.

</details>
<details>
<summary><b>8. Spatial Relations</b></summary>
Embedding models may struggle to differentiate between sentences that describe different spatial arrangements. This can cause visual generation tasks to produce images with incorrect object placements or orientations.

</details>

### Step 3: Generating failure instances
For example, if we want to generate new failure instances with the systematic failure negation:
Negation: Embedding models may not correctly capture the negative context in a sentence, leading to similarities between sentences with and without negation. This can result in incorrect visual representations, as the presence or absence of an action is significant in image or video generation.

We start a new conversastion with GPT-4 with the following message
```
Write down 41 additional pairs of prompts that an embedding model with the following failure mode might encode similarly, even though they would correspond to different images if used as captions. Use the following format:
("prompt1", "prompt2"),
("prompt1", "prompt2"),
You will be evaluated on how well you actually perform. Your sentence structure and length can be creative; extrapolate based on the failure mode you’ve summarized. Be both creative and cautious.
Failure Mode:
Negation: Embedding models may not correctly capture the negative context in a sentence, leading to similarities between sentences with and without negation. This can result in incorrect visual representations, as the presence or absence of an action is significant in image or video generation.
```

GPT-4 should output responses like:
<details>
<summary><b>See examples here</b></summary>
("A dog chasing a cat", "A dog not chasing a cat"),
("A man holding an umbrella", "A man not holding an umbrella"),
("A woman reading a book", "A woman not reading a book"),
("A kid playing with a ball", "A kid not playing with a ball"),
("A bird flying in the sky", "A bird not flying in the sky"),
("A fish swimming in a bowl", "A fish not swimming in a bowl"),
("A chef cooking in the kitchen", "A chef not cooking in the kitchen"),
("A car driving on a road", "A car not driving on a road"),
("A tree shedding leaves", "A tree not shedding leaves"),
("A couple dancing in the rain", "A couple not dancing in the rain"),
("A boy flying a kite", "A boy not flying a kite"),
("A person painting a wall", "A person not painting a wall"),
("A runner crossing the finish line", "A runner not crossing the finish line"),
("A teacher teaching in the classroom", "A teacher not teaching in the classroom"),
("A lion hunting its prey", "A lion not hunting its prey"),
("A baby crying in the crib", "A baby not crying in the crib"),
("A flower blooming in the garden", "A flower not blooming in the garden"),
("A monkey swinging from a tree", "A monkey not swinging from a tree"),
("A sailor navigating the sea", "A sailor not navigating the sea"),
("A girl blowing out birthday candles", "A girl not blowing out birthday candles"),
("A spider spinning a web", "A spider not spinning a web"),
("A football player scoring a goal", "A football player not scoring a goal"),
("A cat catching a mouse", "A cat not catching a mouse"),
("A bee collecting pollen from flowers", "A bee not collecting pollen from flowers"),
("A snowman melting in the sun", "A snowman not melting in the sun"),
("A cyclist riding down the hill", "A cyclist not riding down the hill"),
("A chef chopping vegetables", "A chef not chopping vegetables"),
("A musician playing a guitar", "A musician not playing a guitar"),
("A snake slithering in the grass", "A snake not slithering in the grass"),
("A photographer taking a picture", "A photographer not taking a picture"),
("A horse jumping over a hurdle", "A horse not jumping over a hurdle"),
("A student studying for an exam", "A student not studying for an exam"),
("A cloud casting a shadow", "A cloud not casting a shadow"),
("A turtle hiding in its shell", "A turtle not hiding in its shell"),
("A snowflake falling from the sky", "A snowflake not falling from the sky"),
("A ball bouncing on the ground", "A ball not bouncing on the ground"),
("A firefly glowing in the dark", "A firefly not glowing in the dark"),
("A king wearing a crown", "A king not wearing a crown"),
("An apple falling from a tree", "An apple not falling from a tree"),
("A butterfly emerging from a cocoon", "A butterfly not emerging from a cocoon"),
("A clock ticking on the wall", "A clock not ticking on the wall")
</details>

