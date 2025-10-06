import React, { useState, useRef, useEffect } from 'react';

interface ConfirmButtonProps {
  holdDuration: number;
  onConfirm: () => void;
  children: React.ReactNode;
  minHoldDuration?: number;
  confirmedColor?: string;
  progressColor?: string;
  textColor?: string;
  textColorHover?: string;
  baseColor?: string;
}

const ConfirmButton: React.FC<ConfirmButtonProps> = ({
  holdDuration,
  onConfirm,
  children,
  minHoldDuration = 300,
  confirmedColor = '#4CAF50',
  progressColor = "grey",
  baseColor = '#f0f0f0',
  textColor = "black",
  textColorHover = "white"
}) => {
  const [progress, setProgress] = useState(0);
  const [isHolding, setIsHolding] = useState(false);
  const [isCounting, setIsCounting] = useState(false);
  const [isConfirmed, setIsConfirmed] = useState(false);
  const [helperText, setHelperText] = useState('Pressione e segure para confirmar');
  const [failedAttempts, setFailedAttempts] = useState(0);

  const holdTimerRef = useRef<NodeJS.Timeout | null>(null);
  const progressTimerRef = useRef<NodeJS.Timeout | null>(null);
  const minHoldTimerRef = useRef<NodeJS.Timeout | null>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    return () => {
      clearTimers();
    };
  }, []);

  const clearTimers = () => {
    if (holdTimerRef.current) clearTimeout(holdTimerRef.current);
    if (progressTimerRef.current) clearInterval(progressTimerRef.current);
    if (minHoldTimerRef.current) clearTimeout(minHoldTimerRef.current);
  };

  const startHold = () => {
    setIsHolding(true);
    setIsConfirmed(false);
    setProgress(0);
    setHelperText('Segurando...');

    minHoldTimerRef.current = setTimeout(() => {
      setIsCounting(true);

      const startTime = Date.now();
      const endTime = startTime + holdDuration;

      progressTimerRef.current = setInterval(() => {
        const now = Date.now();
        const newProgress = Math.min(((now - startTime) / holdDuration) * 100, 100);
        setProgress(newProgress);

        if (now >= endTime) {
          handleConfirm();
        }
      }, 10);
    }, minHoldDuration);
  };

  const handleConfirm = () => {
    clearTimers();
    onConfirm();
    setIsConfirmed(true);
    setIsCounting(false);
    setIsHolding(false);
    setProgress(100);
    setHelperText('Confirmado!');

    setTimeout(() => {
      setProgress(0);
      setIsConfirmed(false);
      setHelperText('Pressione e segure para confirmar');
    }, 1500);
  };

  const resetState = () => {
    if (isConfirmed) return;
    clearTimers();

    if (isHolding) {
      setFailedAttempts(prev => prev + 1);
      if (failedAttempts + 1 >= 3) {
        setHelperText('Você precisa segurar o botão para confirmar');
      } else {
        setHelperText('Soltou cedo! Tente novamente.');
      }
    }

    setIsHolding(false);
    setIsCounting(false);
    setProgress(0);
  };

  const handleMouseDown = () => startHold();
  const handleMouseUp = () => resetState();
  const handleTouchStart = (e: React.TouchEvent) => {
    e.preventDefault();
    startHold();
  };
  const handleTouchEnd = () => resetState();

  const getButtonColor = () => {
    if (isConfirmed) return confirmedColor;
    return baseColor;
  };

  const getTextColor = () => {
    if (isConfirmed) return 'white';
    return isHolding ? textColorHover : textColor;
  };

  return (
    <div style={{ width: "100%" }}>
      <button
        ref={buttonRef}
        onMouseDown={handleMouseDown}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onTouchStart={handleTouchStart}
        onTouchEnd={handleTouchEnd}
        aria-label="Botão de confirmação. Pressione e segure para confirmar a ação"
        role="button"
        style={{
          width: "100%",
          position: 'relative',
          overflow: 'hidden',
          padding: '10px 20px',
          border: '1px solid #ccc',
          borderRadius: '4px',
          backgroundColor: getButtonColor(),
          cursor: 'pointer',
          outline: 'none',
          color: textColor,
          transition: isConfirmed
            ? 'background-color 0.3s ease'
            : 'background-color 0.2s, width 0.1s linear',
        }}
      >
        {isCounting && !isConfirmed && (
          <div
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              height: '100%',
              width: `${progress}%`,
              backgroundColor: progressColor,
              transition: 'width 0.1s linear',
            }}
          />
        )}

        <span
          style={{
            position: 'relative',
            zIndex: 1,
            color: getTextColor(),
            transition: 'color 0.3s ease',
          }}
        >
          {isConfirmed ? 'Confirmado!' : children}
        </span>
      </button>

      <div
        style={{
          marginTop: '8px',
          fontSize: '0.85rem',
          color: '#666',
          textAlign: 'center',
        }}
      >
        {helperText}
      </div>
    </div>
  );
};

export default ConfirmButton;
