"USE STRICT";
app.controller("busController", function($scope, $location, dbService){
	//Listando
	$scope.getListBus = function(){
		dbService.runAsync("SELECT * FROM onibus", function(data){
			$scope.pessoas = data;
		});
	}

	/*//Salvando
	$scope.salvar = function(){
		if($scope.pessoa.id){
			//Editar
			var id = $scope.pessoa.id;
			delete $scope.pessoa.id;
			delete $scope.pessoa.$$hashKey; //Apaga elemento $$hashKey do objeto
			dbService.update('pessoas', $scope.pessoa, {id: id}); //entidade, dados, where
		}else{
			//nova
			dbService.insert('pessoas', $scope.pessoa); // entidade, dados
		}
		$scope.pessoa = {};
		$scope.listaPessoas();
		$('#modalPessoa').modal('hide');
	}

	//Abrindo para editar
	$scope.editar = function(dados){
		$scope.pessoa = dados;
		$('#modalPessoa').modal('show');
	}

	//Excluindo
	$scope.excluir = function(dados){
		if(confirm("Deseja realmente apagar o cadastro de "+dados.nome+"?")){
			dbService.update('pessoas', {ativo:0}, {id: dados.id});
			$scope.listaPessoas();
		}
	}
	*/
	//Searchig By Stop Bus
	$scope.searchByStopBus = function(stop_number){
		dbService.runAsync("select o.numero_onibus,o.nome,o.empresa from onibus o ,passar p where p.numer_parada = " + stop_number + " and p.numero_onibus = o.numero_onibus", function(data){
			$scope.pessoas = data;
		});
	}

	//Searching By Street
	$scope.searchByStreet = function(street){
		dbService.runAsync("SELECT  O.numero_onibus , O.nome,O.empresa FROM onibus O, parada P, passar Q WHERE Q.numero_onibus = O.numero_onibus AND P.numero_parada= Q.numer_parada AND P.rua LIKE '%"+street+"'", function(data){
			$scope.pessoas = data;
		});
	}

});