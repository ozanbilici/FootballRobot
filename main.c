/*
 * main.c
 *
 *  Created on: Oct 22, 2015
 *      Author: ozan
 */

#include <avr/io.h>
#include <util/delay.h>


char data[16];
volatile int i = 0;
volatile int newData = 0;

// PD4 - Done
// PC6 - PWM for dribbler motor

ISR(USART1_RX_vect){
	  unsigned char ch = UDR1;

	  if(ch >= ' ' && ch <= '~'){
	    data[i] = ch;
	    i++;
	  }

	  if(ch == '\n' || ch == '\r'){
	    data[i] = '\0';
	    i = 0;
	    newData = 1;
	    return;
	  }
}

ISR(PCINT0_vect) {
	if(((PINB & 0b00010000) >> 4) == 0) {
		reset_charge();
	}
}

void init_uart(unsigned int baud) {
	// enable the global interupt
	SREG |= (1 << 7);

	// set the baud rate - 19200
	//UBRRH1 = (unsigned char) (baud >> 8);
	//UBRRL1 = (unsigned char) (baud);
	UBRR1 = 51;

	// enable rx interupt, receiver and transmitter
	UCSR1B = (1 << 7) | (1 << 4) | (1 << 3) ;

	// set frame format : 8 data 1 stop bit no parity
	UCSR1C =  (3 << 1);
}

void sendData(char* data) {
	PORTD &= ~0x10000000; // reset the receiver enable
	PORTD |= 0x01000000; // set the transmit enable

	while(*data) {
		while(!( UCSR1A & (1<<UDRE1)));
		UDR1 = *data;
		*data++;
	}
	 _delay_ms(5);
	PORTD &= ~0x01000000; // reset the transmit enable
	PORTD |= 0x10000000; // set the receiver enable
}
// reset the all leds
void resetLed() {
	PORTF |= 0b11110011; // reset all led pins
}

// set the led what you want to color
void setLed(int value) {
	resetLed();
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
		PORTF &= ~0b00000001;
		break;
	case 2:
		PORTF &= ~0b00000010;
		break;
	case 3:
		PORTF &= ~0b00010000;
		break;
	case 4:
		PORTF &= ~0b00100000;
		break;
	case 5:
		PORTF &= ~0b01000000;
		break;
	case 6:
		PORTF &= ~0b10000000;
		break;

	}
}

void set_charge() {
	PORTD |= 0b00100000;
}

void reset_charge() {
	PORTD &= 0b11011111;
}

void set_kick() {
	PORTD |= 0b00010000;
}

void reset_kick() {
	PORTD &= 0b11101111;
}

int ifBall() {
	if(((PINE & 0x01000000) >> 6) == 1) {
		return 1;
	} else {
		return 0;
	}
}

int main() {
	// Setting Clock

	// Use external clock
	CLKPR = 0x80;
	CLKPR = 0x00;

	// set the direction of led pins as output
	DDRF |= 0b11110011;

    // set the ball detection pin as input
	DDRE &= 0b10111111;
	PORTE &= 0b10111111; // pull up resistor off

	// set the de,re, kick and charge pin as output
	DDRD |= 0b11110000;
	PORTD |= 0x10000000; // set the receiver enable


	//initialization uart
	init_uart();

	// Set PB4 as input for checking if it is done
	DDRB &= ~0b00010000;
	PCMSK0 = (1 << 4); // set interupt mask for PB4
	PCICR = 0x01; // enable PCINT

	resetLed();

	while(1) {
		if(newData == 1) {
			if((data[0] == '5') && (data[1] == ':')) {
				if((data[3] == 'k') && (data[4] == 'i')) {
					set_kick();
					setLed(1);
				} else if((data[3] == 'c') && (data[4] == 'h')) {
					reset_kick();
					set_charge();
					setLed(2);
				} else if((data[3] == 'i') && (data[4] == 'b')) {
					if(ifBall() == 1) {
						sendData("yes\n\r");
					} else {
						sendData("no\n\r");
					}

					setLed(3);
				}
			}

			// data commands already read
			newData = 0;
		}

		if(ifBall() == 1) {
			setLed(1);
		} else {
			setLed(2);
		}
	}


	return 1;
}


