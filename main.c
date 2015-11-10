
#define F_CPU 16000000UL

#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

// variables
volatile int newData = 0;
char data[16];
volatile int i = 0;
volatile int charger = 0;
int startSaving = 0;

void UsartInit() {
	// Set the USART Pin as output
	DDRD &= ~(0b11001000);
	DDRD |= 0b11000100;

	PORTD &= ~(0x80);

	UCSR1A = 2;
	// baud rate : 19200
	UBRR1 = 12;
	// enable Read interrupt, receiver and transmitter
	UCSR1B = (1<<RXEN1)|(1<<TXEN1);
	// set frame format : 8 data 1 stop bit no parity
	UCSR1C = (1<<USBS1)|(3<<UCSZ10);

	UCSR1B |= (1 << 7);
}

void UsartSend(const char* data) {
  PORTD |= 0b01000000;

  //data = "derp\n\0";

  while(*data){
	  while(!( UCSR1A & (1<<UDRE1)));
	  UDR1 = *data;
	  data++;
  }

  _delay_ms(5);
  PORTD &= 0b00111111;
}

void PWMInit() {
	// set PC6 as output
	DDRC |= (1 << 6);

	TCCR3A &= ~(0b11110011);
	TCCR3A |= 0b11000011;

	TCCR3B &= (0b01110000);
	TCCR3B |=  (1 << 3) | (3 << 0); // 62 500 Hz

	OCR3A =  0x3ff;
}

void IOInit() {
	//disable JTAG, needed to use some of the pins on the MCU
	MCUCR|= (1<<JTD); //in order to change this value, it is needed to
	MCUCR|= (1<<JTD); //overwrite this value twice during 4 clock cycles

	// set the direction of led pins as output
	DDRF = 0b11110011;

	// set kick and charge pin as output
	DDRD |= 0b00110000;

	// set the done pin as input and initialize the interrupt
	DDRB &= ~(0b00010000);
	PCMSK0 |= (0b00010000);
	PCICR = 0x01;

	// ball detection set as input
	DDRE &= ~(1 << 6);
}

// set the led what you want to color
void setLed(int value) {
	//
	// value = 1 => LED2Green
	// value = 2 => LED2Red
	// value = 3 => LED2Blue
	// value = 4 => LED1Green
	// value = 5 => LED1Red
	// value = 6 => LED1Blue
	//

	switch(value) {
		case 1:
		PORTF = 0b11110010;
		break;
		case 2:
		PORTF = 0b11110001;
		break;
		case 3:
		PORTF = 0b11100011;
		break;
		case 4:
		PORTF = 0b11010011;
		break;
		case 5:
		PORTF = 0b10110011;
		break;
		case 6:
		PORTF = 0b01110011;
		break;

	}
}


ISR(USART1_RX_vect){

	unsigned char character = UDR1;

	if(character == '5') {
		i = 0;
		startSaving = 1;
	}

	if(startSaving == 1) {
		if(character >= ' ' && character <= '~'){
			data[i] = character;
			i++;
		}

		if(character == '\n' || character == '\r'){
			data[i] = '\0';
			i = 0;
			newData = 1;
			startSaving = 0;

			return;
		}
	}
}

ISR(PCINT0_vect) {
	if(((PORTD >> 4) & 0x1) == 0) {
		PORTD &= ~(1 << 4);
	}
}


int main() {
	// Clock Initialize
	//CLKPR = 0x80;
	//CLKPR = 0x00;
	//CLKSEL0 = 0x05;
	/*CLKSEL0 = 0x05;
	CLKSEL1 = 0x08;
	while(!(CLKSTA & 0x01));*/



	// USART Initialize
	UsartInit();

	// IO Pins Initialize
	IOInit();

	// PWM Initialize
	PWMInit();


	// Global Interrupt Enable
	SREG |= (1 << 7);


	setLed(1);


	//
	// 5:kr : kick run
	// 5:ks : kick stop
	// 5:cr : charge run
	// 5:cs : charge stop
	// 5:if : dribler stop
	// 5:dr : dribler run
	// 5:ds : dribler stop
	//

	while(1) {

		if(newData == 1) {

			if((data[0] == '5') && (data[1] == ':')) {

				if((data[2] == 'k') && (data[3] == 'r')) {
					// stop charging
					PORTD &= ~(1 << 4);

					// kick the ball
					PORTD |= (1 << 5);
					setLed(4);
				}
				else if((data[2] == 'k') && (data[3] == 's')) {
					// stop charging
					PORTD &= ~(1 << 4);

					// stop kicking
					PORTD &= ~(1 << 5);
					setLed(5);
				}
				else if((data[2] == 'c') && (data[3] == 'r')) {
					charger = 1;
					PORTD &= ~(1<<5); // close kicking
					PORTD |= (1 << 4); // start charging
					setLed(4);

				}
				else if((data[2] == 'c') && (data[3] == 's')) {
					charger = 1;
					PORTD &= ~(1<<5); // close kicking
					PORTD &= ~(1 << 4); // start charging
					setLed(5);

				}
				else if((data[2] == 'i') && (data[3] == 'b')) {
					setLed(4);
					if(((PORTE >> 6) & 0x01) == 1) {
						UsartSend("no\r\n");
						} else {
						UsartSend("yes\r\n");
					}
				} else if((data[2] == 'd') && (data[3] == 'r')) {
					setLed(4);
					OCR3A =  723;
				} else if((data[2] == 'd') && (data[3] == 's')) {
					setLed(5);
					OCR3A =  0x3ff;
				}
			}

			newData = 0;
		}

	}

	return 1;
}
