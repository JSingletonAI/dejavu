
# Run the experiments
run-dejavu-add:
	python run_experiments.py --technique_type dejavu --method add

run-dejavu-search:
	python run_experiments.py --technique_type dejavu --method search --output_folder results/ --top_k 30

run-dejavu-plus-add:
	python run_experiments.py --technique_type dejavu --method add --is_graph

run-dejavu-plus-search:
	python run_experiments.py --technique_type dejavu --method search --is_graph --output_folder results/ --top_k 30

run-rag:
	python run_experiments.py --technique_type rag --chunk_size 500 --num_chunks 1 --output_folder results/

run-full-context:
	python run_experiments.py --technique_type rag --chunk_size -1 --num_chunks 1 --output_folder results/

run-langmem:
	python run_experiments.py --technique_type langmem --output_folder results/

run-zep-add:
	python run_experiments.py --technique_type zep --method add --output_folder results/

run-zep-search:
	python run_experiments.py --technique_type zep --method search --output_folder results/

run-openai:
	python run_experiments.py --technique_type openai --output_folder results/
