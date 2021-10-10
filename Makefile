setup:
	@ echo "Setup process..."
	@ ( \
	   echo "Creating virtualenv..."; \
	   python -m venv venv; \
	   echo "Activating virtualenv..."; \
       source $(PWD)/venv/bin/activate; \
	   echo "Installing packages..."; \
	   pip install --upgrade pip; \
       pip install -r requirements.txt; \
    )


run:
	@ echo "Activating Python virtualenv..."
	@ source $(PWD)/venv/bin/activate;
	@ echo "Run inzidenz-ampel..."
	@ python incidence.py;

venv:
	@ echo "Creating a new virtualenv..."
	@ python3 -m venv venv;

clean:
	@ echo "Cleaning..."
	@ rm -rf cache.json
	@ rm -rf venv
	@ echo "All done!"