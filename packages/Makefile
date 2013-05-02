subsystem:
	$(MAKE) -C deb
	$(MAKE) -C rpm

clean:
	$(MAKE) -C deb clean
	$(MAKE) -C rpm clean
	rm -rf *.deb *.tar.gz *.dsc *.changes
	rm -rf *.rpm
