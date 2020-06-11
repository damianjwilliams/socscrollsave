all: gui

gui:
	$(MAKE) -C socscrollsave/res

run:
	python -m socscrollsave -v

doc:
	$(MAKE) html -C docs

.PHONY: clean
clean:
	$(MAKE) clean -C socscrollsave/res
	$(MAKE) clean -C docs
	rm -rf socscrollsave/*.pyc
	rm -rf socscrollsave/__pycache__
	rm -rf data