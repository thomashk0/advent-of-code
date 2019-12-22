-include target/debug/libaoc_bindings.d
-include target/release/libaoc_bindings.d

LIBS := intcpu/libaoc_bindings_debug.so intcpu/libaoc_bindings.so

.PHONY: wheel
wheel: $(LIBS)
	python setup.py bdist_wheel

target/debug/libaoc_bindings.so:
	cargo build

target/release/libaoc_bindings.so:
	cargo build --release

intcpu/libaoc_bindings_debug.so: target/debug/libaoc_bindings.so
	cp $< $@

intcpu/libaoc_bindings.so: target/release/libaoc_bindings.so
	cp $< $@
