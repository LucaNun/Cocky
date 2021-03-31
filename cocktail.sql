-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Erstellungszeit: 27. Mrz 2021 um 12:19
-- Server-Version: 10.4.17-MariaDB
-- PHP-Version: 8.0.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `cocktail`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `inhalte`
--

CREATE TABLE `inhalte` (
  `Inhalts.ID` int(11) NOT NULL,
  `Pumpen.ID` int(11) DEFAULT NULL,
  `Bezeichnung` tinytext NOT NULL,
  `Beschreibung` text NOT NULL,
  `Alkohol` tinyint(1) NOT NULL,
  `Manuell` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Daten für Tabelle `inhalte`
--

INSERT INTO `inhalte` (`Inhalts.ID`, `Pumpen.ID`, `Bezeichnung`, `Beschreibung`, `Alkohol`, `Manuell`) VALUES
(1, 1, 'Gin', 'halt Gin', 1, 0),
(2, NULL, 'Eiswürfel', 'gefrorenes Wasser', 0, 1),
(3, NULL, 'Limettenscheibe', 'ist sauer', 0, 1),
(4, NULL, 'Gurkenscheibe', 'ist grün', 0, 1),
(5, NULL, 'Tonic Water', 'bitteres Wasser', 0, 0),
(6, 3, 'Ginger Bier', '.........', 1, 0),
(7, 4, 'Limettensaft', '.........', 0, 0),
(8, 5, 'Wodka', '.........', 1, 0);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `mischungen`
--

CREATE TABLE `mischungen` (
  `Mischungs.ID` int(11) NOT NULL,
  `Bezeichnung` tinytext NOT NULL,
  `Beschreibung` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Daten für Tabelle `mischungen`
--

INSERT INTO `mischungen` (`Mischungs.ID`, `Bezeichnung`, `Beschreibung`) VALUES
(1, 'Gin Tonic', 'Halt Gin Tonic'),
(2, 'Moscow Mule', '...........');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `mischungen&inhalte`
--

CREATE TABLE `mischungen&inhalte` (
  `Mischungs.ID` int(11) NOT NULL,
  `Inhalts.ID` int(11) NOT NULL,
  `Menge` tinyint(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Daten für Tabelle `mischungen&inhalte`
--

INSERT INTO `mischungen&inhalte` (`Mischungs.ID`, `Inhalts.ID`, `Menge`) VALUES
(1, 1, 40),
(1, 5, 70),
(2, 6, 16),
(2, 7, 10),
(2, 2, 0),
(2, 4, 2),
(2, 8, 70);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `pumpen`
--

CREATE TABLE `pumpen` (
  `Pumpen.ID` int(11) NOT NULL,
  `PIN` tinyint(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Daten für Tabelle `pumpen`
--

INSERT INTO `pumpen` (`Pumpen.ID`, `PIN`) VALUES
(1, 24),
(2, 21),
(3, 26),
(4, 19),
(5, 13),
(6, 23),
(7, 25),
(8, 12),
(9, 16),
(10, 20);

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `inhalte`
--
ALTER TABLE `inhalte`
  ADD PRIMARY KEY (`Inhalts.ID`);

--
-- Indizes für die Tabelle `mischungen`
--
ALTER TABLE `mischungen`
  ADD PRIMARY KEY (`Mischungs.ID`);

--
-- Indizes für die Tabelle `pumpen`
--
ALTER TABLE `pumpen`
  ADD PRIMARY KEY (`Pumpen.ID`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `inhalte`
--
ALTER TABLE `inhalte`
  MODIFY `Inhalts.ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT für Tabelle `mischungen`
--
ALTER TABLE `mischungen`
  MODIFY `Mischungs.ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT für Tabelle `pumpen`
--
ALTER TABLE `pumpen`
  MODIFY `Pumpen.ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
