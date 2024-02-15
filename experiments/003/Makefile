# This is the main makefile for the experiments. It will run all the experiments in the correct order.



# This one runs the experiments on the full dataset.
SAMPLES_FLAG=--random-sample-size=-1

# Specify the size one in this one to run this over a subset of the data.
# SAMPLES_FLAG=--random-sample-size=2

# Collect Api Payload
../apipayload.json:
	python ../collect_api_payload.py


output/postprocessed_ocr_provider_data.json: ../apipayload.json
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
# Bandwidth step should be 5, I am setting it up to 50 for speedup

# Add the language models you want to use, current option is [cot, simple]
# All the possible methods are cot cot-test1 cot-test2 cot-test3 cot-test4 cot-test5 simple simple-test1 simple-test2 simple-test3 gpt4-vision
# However we are only using the ones that has showed promising results.
output/lm_post_processed.json: output/recognized_indentations.json
	python lm_post_correction.py  \
		--input-file output/recognized_indentations.json \
		--output-file output/lm_post_processed.json \
		--post-correction-methods none cot-test1 cot-test5 simple-test2 simple-test3 gpt4-vision


# Running this one runs the entire pipeline and then dumps the results(No Evaluation)
output/dumped_outputs: output/lm_post_processed.json
	python dump_results.py \
		--input-file output/lm_post_processed.json \
		--images-dir ../images \
		--output-dir output/dumped_outputs


# Running this one runs the entire pipeline and then Gives the evaluation results(No Dumping results)
output/eval_results.txt: output/lm_post_processed.json
	python generate_evaluation_results.py \
		--input-file output/lm_post_processed.json \
		--output-file output/eval_results.txt



.PHONY: remove-results
remove-results:
	rm -f output/eval_results.txt
	rm -rf output/dumped_outputs

.PHONY: remove-output
remove-output:
	rm -rf output/*


.PHONY: remove-all-data
remove-all:
	rm -rf output/*
	rm -f ../apipayload.json


.PHONY: all-results
all-results: output/eval_results.txt output/dumped_outputs