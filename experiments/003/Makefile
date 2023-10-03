# SAMPLES_FLAG=--random-sample-size=-1
SAMPLES_FLAG=--random-sample-size=2


output/postprocessed_ocr_provider_data.json:
	mkdir -p output
	python post_process_ocr_results.py \
		--input-file ../apipayload.json \
		--output-file output/postprocessed_ocr_provider_data.json \
		--included-providers Azure \
		${SAMPLES_FLAG} \
		# GCV AWS Azure MP

output/recognized_indentations.json: output/postprocessed_ocr_provider_data.json
	python recognize_indentations.py  \
		--input-file output/postprocessed_ocr_provider_data.json \
		--output-file output/recognized_indentations.json \
		--bandwidth-min 0 \
		--bandwidth-max -1 \
		--bandwidth-step 5

output/lm_post_processed.json: output/recognized_indentations.json
	python lm_post_correction.py  \
		--input-file output/recognized_indentations.json \
		--output-file output/lm_post_processed.json \
		--post-correction-methods cot simple


output/recognition_outputs: output/lm_post_processed.json
	python dump_recognition_results.py \
		--input-file output/lm_post_processed.json \
		--images-dir ../images \
		--output-dir output/recognition_outputs

output/eval_results.txt: output/recognized_indentations.json
	python generate_evaluation_results.py \
		--input-file output/recognized_indentations.json \
		--output-file output/eval_results.txt




# This one is just to quickly generate results from the LM json. I will integrate this into the main eval script later.
output/final_eval.txt: output/lm_post_processed.json
	python lm_post_correction_eval.py  \
		--input-file output/lm_post_processed.json \
		--output-file output/final_eval.txt