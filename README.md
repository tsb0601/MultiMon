### Running the Code

#### Step 1: Scraping the Data

You will need to run the `scrape.py` file. This file contains arguments that can be adjusted according to your needs:

- `steer`: Steering direction for the self-driving car (default is "self-driving cars").
- `corpus_data`: Corpus data to scrape (default is "MS-COCO").
- `num_output`: Number of entries we want (default is 150).
- `api_key`: API Key for your openAI account (default is empty).
- `do_steer`: Execute steering direction (default is False).

To run the script, navigate to the directory containing `scrape.py` in your terminal, and type:

</pre>
<code>
python scrape.py --steer [your_value] --corpus_data [your_value] --num_output [your_value] --api_key [your_value] --do_steer [your_value]
</code>
<pre>
For exanmple, if we want to scrape 150 entries from MS-COCO without steering, we run
</pre>
<code>
python scrape.py --corpus_data MS-COCO --num_output 150
</code>
<pre>
