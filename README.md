# Mass-Producing Failures of Multimodal Models

![The MultiMon pipeline](Pipeline/pipeline.png)

Authors: Shengbang Tong*, Erik Jones*, Jacob Steinhardt

### Running and Using MultiMon

#### Step 1: Scraping from corpus data

You will need to run the `scrape.py` file. This file contains arguments that can be adjusted according to your needs:

- `steer`: Steering direction for the self-driving car (default is "self-driving cars").
- `corpus_data`: Corpus data to scrape (default is "MS-COCO").
- `num_output`: Number of entries we want (default is 150).
- `api_key`: API Key for your openAI account (default is empty).
- `do_steer`: Execute steering direction (default is False).

To run the script, navigate to the directory containing `scrape.py` in your terminal, and type:

```
python scrape.py --steer [your_value] --corpus_data [your_value] --num_output [your_value] --api_key [your_value] --do_steer [your_value]
```
For exanmple, if we want to scrape 150 entries from MS-COCO without steering, we run
```
python scrape.py --corpus_data MS-COCO --num_output 150
```

#### Step 2: Categorizing systematic failure
After scraping the corpus data, replace the failure instances with the scraped failure instances and prompts LLM (GPT-4 or Claude)
```
I will provide a series of data for you to remember. Subsequently, I will ask you some questions to test your performance! Here are some pairs of prompts for you to memorize. 
[Copy paste the failure instances scraped in csv file from previous step]

I’m trying to find failures with an embedding model. The above are some pairs of sentences that it encodes very similarly, even though they’re conveying different concepts. Using these specific examples, are there any general types of failures you notice the embedding is making, or any common features that the embedding fails to encode? Try to give failures that are specific enough that someone could reliably produce examples that the embedding would encode similarly, even though it shouldn’t. Please try to give as many general failures as possible. Please focus on differences that are important visually, as these embeddings are later used to generate images, or videos. In your failure modes, please explain clearly why the failure would lead to problems for future tasks related to visual generation.Please summarize as many as you can and stick to the examples.
```


