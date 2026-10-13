import React from 'react';
import { SceneTiming } from '../timeline';
import { Frage, Intro, Personen, Rahmen } from './part1';
import { Hebamme, Mathematik } from './part2';
import { Def1, Fluss, Traum, Zwillinge } from './part3';
import { Apologie, Exkurs, Fluss2, Kritik1, Peritrope, Zukunft } from './part4';
import { Def2, Dialog, Pferd } from './part5';
import { Elf, Richter, Taubenschlag, Wachs } from './part6';
import { Aporie, Def3, Logos, Merkmal, Silben } from './part7';
import { Deutung, Gettier, Schluss } from './part8';

export const SCENES: Record<string, React.FC<{ t: SceneTiming }>> = {
  intro: Intro,
  rahmen: Rahmen,
  personen: Personen,
  frage: Frage,
  mathematik: Mathematik,
  hebamme: Hebamme,
  def1: Def1,
  fluss: Fluss,
  zwillinge: Zwillinge,
  traum: Traum,
  kritik1: Kritik1,
  apologie: Apologie,
  peritrope: Peritrope,
  exkurs: Exkurs,
  zukunft: Zukunft,
  fluss2: Fluss2,
  pferd: Pferd,
  def2: Def2,
  dialog: Dialog,
  wachs: Wachs,
  elf: Elf,
  taubenschlag: Taubenschlag,
  richter: Richter,
  def3: Def3,
  silben: Silben,
  logos: Logos,
  merkmal: Merkmal,
  aporie: Aporie,
  deutung: Deutung,
  gettier: Gettier,
  schluss: Schluss,
};
