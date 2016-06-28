//Programa : Teste NRF24L01 - Receptor - Led
//Autor : Adilson Thomsen

#include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"

//Armazena os dados recebidos
int recebidos[1];

//Inicializa a placa nos pinos 9 (CE) e 10 (CS) do Arduino
RF24 radio(9,10);

//Define o endereco para comunicacao entre os modulos
const uint64_t pipe = 0xE14BC8F482LL;

//Define os pinos dos leds
int LED1 = 5;
int LED2 = 3;

void setup()
{
  //Define os pinos dos leds como saida
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);

  //Inicializa a serial
  Serial.begin(57600);
  
  //Inicializa a comunicacao
  radio.begin();
  //Entra em modo de recepcao
  radio.openReadingPipe(1,pipe);
  radio.startListening();
}

void loop()
{
 if (radio.available())
  {
    bool done = false;    
    while (!done)
    {
      done = radio.read(recebidos, 1);
      Serial.print("Dados recebidos : ");    
      Serial.println(recebidos[0]);
      
      //Se recebeu o numero 1, acende o LED1
      if (recebidos[0] == 1)
      {
        delay(10);
        digitalWrite(LED1, HIGH);
      }
      else 
      {
       digitalWrite(LED1, LOW);
      }
      
      //Se recebeu o numero 2, acende o LED2
      if (recebidos[0] == 2)
      {
        delay(10);digitalWrite(LED2, HIGH);
      }
      else 
      {
        digitalWrite(LED2, LOW);
      }
      delay(100);
    }
  }
  else
  {
  Serial.println("Aguardando dados...");
  }
}
