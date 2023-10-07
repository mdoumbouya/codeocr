# This is the main makefile for the experiments. It will run all the experiments in the correct order.



# This one runs the experiments on the full dataset.
SAMPLES_FLAG=--random-sample-size=-1

# Specify the size one in this one to run this over a subset of the data.
# SAMPLES_FLAG=--random-sample-size=15


output/postprocessed_ocr_provider_data.json:
	mkdir -p output
	python post_process_ocr_results.py \
		--input-file ../apipayload.json \
		--output-file output/postprocessed_ocr_provider_data.json \
		--included-providers Azure \
		${SAMPLES_FLAG} \
		# GCV AWS Azure MP

# You can put bandwidth as -1 to run no custom bandwidth, in that case it will only run [none, estimated]
output/recognized_indentations.json: output/postprocessed_ocr_provider_data.json
	python recognize_indentations.py  \
		--input-file output/postprocessed_ocr_provider_data.json \
		--output-file output/recognized_indentations.json \
		--bandwidth-min 1 \
		--bandwidth-max 200 \
		--bandwidth-step 5

# Add the language models you want to use, current option is [cot, simple]
output/lm_post_processed.json: output/recognized_indentations.json
	python lm_post_correction.py  \
		--input-file output/recognized_indentations.json \
		--output-file output/lm_post_processed.json \
		--post-correction-methods cot simple


output/recognition_outputs: output/lm_post_processed.json
	python dump_results.py \
		--input-file output/lm_post_processed.json \
		--images-dir ../images \
		--output-dir output/dumped_outputs


output/eval_results.txt: output/lm_post_processed.json
	python generate_evaluation_results.py \
		--input-file output/lm_post_processed.json \
		--output-file output/eval_results.txt
