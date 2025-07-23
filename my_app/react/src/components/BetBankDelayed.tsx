// src/components/BetBankDelayed.tsx

import type { GameStateData } from "../types/game-types";
import { formatNumber } from "../utilities/utils";
import "../styles/betting.css";
import { useEffect, useState } from "react";

interface BetBankDelayedProps {
  finalGameState: GameStateData; // Ez a prop most már helyesen van definiálva
  initialBet: number | null;
  initialTokens: number | null;
}

const BetBankDelayed: React.FC<BetBankDelayedProps> = ({
  finalGameState,
  initialBet,
  initialTokens,
}) => {
  const [displayedBet, setDisplayedBet] = useState<number | null>(initialBet);
  const [displayedTokens, setDisplayedTokens] = useState<number | null>(
    initialTokens
  );

  useEffect(() => {
    setDisplayedTokens(initialTokens);
    setDisplayedBet(initialBet);


    const timeoutId: NodeJS.Timeout = setTimeout(() => {
      console.log("--- DEBUG --- BetBankDelayed: Késleltetés utáni frissítés.");
      setDisplayedTokens(finalGameState.tokens);
      setDisplayedBet(finalGameState.player[5]);
    }, 1500);


    return () => {
      clearTimeout(timeoutId);
    };
  }, [finalGameState, initialBet, initialTokens]); // Az initial érték is függőség
  console.log("displayedBet: ", displayedBet);

  const tokensToDisplay =
    displayedTokens !== null ? formatNumber(displayedTokens) : "---";
  const betToDisplay =
    displayedBet !== null ? formatNumber(displayedBet) : "---";
  console.log("betToDisplay: ", betToDisplay);

  return (
    <div>
      <div className="bank">Bet: {betToDisplay}</div>
      <div className="bank">
        Player's bank: <span className="bank-amount">{tokensToDisplay}</span>
      </div>
    </div>
  );
};

export default BetBankDelayed;
