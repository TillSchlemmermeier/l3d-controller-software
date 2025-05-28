all: say_hello world2vox_fortran

say_hello:
	@echo ''
	@echo 'starting make process...'
	@echo ''

world2vox_fortran:
	@echo 'compiling effects...'
	@f2py3 --quiet -c -m gen_outer_shadow_f e_outer_shadow_f.f90

clean:
	@echo 'Cleaning up...'
	$(RM) *.so
	$(RM) *.pyc
