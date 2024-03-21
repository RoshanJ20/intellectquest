import React from 'react';
import './button.css';


const Button = ({ children, className }: { children: React.ReactNode, className?: string }) => {
  return (
    <div>
      <button className={className+' button'}>{children}</button>
    </div>
  )
};
export default Button;