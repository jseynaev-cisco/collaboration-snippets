<?php
error_reporting(E_ALL);

/**
 * @author Jan Seynaeve at Cisco
 */
class AXL
{
	public $soap = null;
	private $server = null;
	private $user = null;
	private $pwd = null;

	function __construct($user, $pwd, $server) {
		$this->user = $user;
		$this->pwd = $pwd;
		$this->server = $server;
		$this->setClient();
	}
	
	function __destruct() {
		unset($this->soap);
	}	
	
	private function setClient() {
		try{
			$context = stream_context_create([
				'ssl' => [
				// set some SSL/TLS specific options
				// for production use, this should be tweaked (commented out, basically)
				'verify_peer' => false,
				'verify_peer_name' => false,
				'allow_self_signed' => true
				]
			]);
			
			$this->soap = new SoapClient(__DIR__ . '/schema/10.5/AXLAPI.wsdl',
					array(
							'trace' => true,
							'exceptions' => true,
							'keep_alive' => false,
							'location' => 'https://'.$this->server.':8443/axl',
							'login' => $this->user,
							'password' => $this->pwd,
							'features' => SOAP_SINGLE_ELEMENT_ARRAYS,
							'cache_wsdl' => WSDL_CACHE_NONE,
							'stream_context' => $context
					));
		}
		catch(Exception $e) {
			echo "AXL setClient | ERROR | ".$e->faultstring;
		}
	}
	
	public function setServer($server) {
		$this->server = $server;
		$this->setClient();
	}
	
	public function setUser($user, $pwd) {
		$this->user = $user;
		$this->pwd = $pwd;
		$this->setClient();		
	}
	
	/**
	 * Do a request
	 * If successful this will return an object with an object 'return' in it, if not a string with the error message is given back
	 * So, to check on success, just try isset($respons->return)
	 */
	public function doRequest($call, $params) {
		try
		{
			$response = NULL;
			if(isset($this->soap))
				$response = $this->soap->$call($params);
			return $response;
		}
		catch(Exception $e) {
			return "AXL doRequest | ERROR | ".$e->faultstring;
		}
	}

	public function getLastRequest() {
		try
		{
			$response = NULL;
			if(isset($this->soap))
				$response = $this->soap->__getLastRequest();
			return $response;
		}
		catch(Exception $e) {
			return "AXL doRequest | ERROR | ".$e->faultstring;
		}
	}
}

?>
