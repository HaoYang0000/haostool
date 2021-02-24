import React, { useState } from "react";
import RouterMap from "./router";
import { IntlProvider } from "react-intl";
import locale_cn from "./translations/cn.json";
import locale_en from "./translations/en.json";

const App = () => {
  const [lang, setLang] = useState("zh_CN");

  const data = {
    zh: locale_cn,
    en: locale_en,
  };
  const getMessages = () => {
    console.log(lang);
    switch (lang) {
      case "zh_CN":
        return locale_cn;
      case "en_US":
        return locale_en;
      default:
        return locale_cn;
    }
  };
  const getLang = () => {
    switch (lang.split("_")[0]) {
      case "en":
        return "en";
      case "zh":
        return "zh";
      default:
        return "zh";
    }
  };

  const handleLangChange = (newLan) => {
    setLang(newLan);
  };

  return (
    <IntlProvider locale={getLang(lang)} messages={getMessages()}>
      <RouterMap handleLangChange={handleLangChange} />
    </IntlProvider>
  );
};

export default App;
