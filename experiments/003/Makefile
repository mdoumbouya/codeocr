# step (1) - download api payload
# assumes that ../apipayload.json exists


# step (2)


data/postprocessed_ocr_provider_data.json:
	mkdir -p data
	python post_process_ocr_results.py \
		--input-file ../apipayload.json \
		--output-file data/postprocessed_ocr_provider_data.json \
		--included-providers Azure
		# GCV AWS Azure MP

data/recognized_indentations.json:
	python recognize_indentations.py  \
		--input-file data/postprocessed_ocr_provider_data.json \
		--output-file data/recognized_indentations.json \
		--bandwidth-min 10 \
		--bandwidth-max 200 \
		--bandwidth-step 5
