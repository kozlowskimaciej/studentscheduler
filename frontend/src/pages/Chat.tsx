import React, { useState } from 'react';
import styled, { keyframes } from 'styled-components';
import Navbar from "../components/common/Navbar";

// Define keyframes for animation
const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

// Styled components
const ChatContainer = styled.div`
  width: 300px;
  margin: auto;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
`;

const Messages = styled.div`
  flex: 1;
  padding: 10px;
  overflow-y: auto;
`;

const ChatBubbleStyled = styled.div<{ isUser: boolean }>`
  margin: 5px 0;
  padding: 10px;
  border-radius: 10px;
  max-width: 80%;
  animation: ${fadeIn} 0.3s ease-in-out;
  background-color: ${(props: { isUser: any; }) => (props.isUser ? '#007bff' : '#f1f0f0')};
  color: ${(props: { isUser: any; }) => (props.isUser ? 'white' : 'black')};
  align-self: ${(props: { isUser: any; }) => (props.isUser ? 'flex-end' : 'flex-start')};
`;

const InputContainer = styled.div`
  display: flex;
  border-top: 1px solid #ccc;
`;

const Input = styled.input`
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 0 0 0 10px;
  outline: none;
`;

const Button = styled.button`
  padding: 10px;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 0 0 10px 0;
  cursor: pointer;

  &:hover {
    background-color: #0056b3;
  }
`;

// Define the interface for ChatBubbleProps
interface ChatBubbleProps {
  text: string;
  isUser: boolean;
}

// Define ChatBubble component with explicit prop types using the ChatBubbleProps interface
const ChatBubble: React.FC<ChatBubbleProps> = ({ text, isUser }: ChatBubbleProps) => (
  <ChatBubbleStyled isUser={isUser}>{text}</ChatBubbleStyled>
);

// Define the type for the message object
interface Message {
  text: string;
  isUser: boolean;
}

export default function Calendar() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>('');

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, isUser: true }]);
      setInput('');

      // Simulate bot response
      setTimeout(() => {
        setMessages((prev: any) => [
          ...prev,
          { text: 'This is a bot response', isUser: false },
        ]);
      }, 1000);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  };

  return (
    <>
      <Navbar />
        <ChatContainer>
          <Messages>
            {messages.map((msg: { text: any; isUser: any; }, index: any) => (
              <ChatBubble key={index} text={msg.text} isUser={msg.isUser} />
            ))}
          </Messages>
          <InputContainer>
            <Input
              type="text"
              value={input}
              onChange={handleInputChange}
              placeholder="Type a message"
            />
            <Button onClick={handleSend}>Send</Button>
          </InputContainer>
        </ChatContainer>
    </>     
  );
}
